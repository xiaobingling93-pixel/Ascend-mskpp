#!/usr/bin/python
# -*- coding: UTF-8 -*-
# -------------------------------------------------------------------------
# This file is part of the MindStudio project.
# Copyright (c) 2025 Huawei Technologies Co.,Ltd.
#
# MindStudio is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
# -------------------------------------------------------------------------

import unittest
import json
import os
from mskpp import mmad, Tensor, Chip, Core, wait_flag, set_flag, vadd
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

FORMAT_TYPE_ND = "ND"
FORMAT_TYPE_NZ = "NZ"
FORMAT_TYPE_NC1HWC0 = "NC1HWC0"


class TestDifferentCoreSync(TestBase):
    TRACE_FILE = 'trace.json'
    HTML_FILE = 'instruction_cycle_consumption.html'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_diff_core_sync_slice_mix(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            chip.enable_metrics()
            gm_x = Tensor("GM", "FP16", [128, 256], format="ND")
            gm_y = Tensor("GM", "FP16", [256, 512], format="ND")
            gm_out = Tensor("GM")
            gm_z = Tensor("GM", "FP32", [128, 512], format="NC1HWC0")
            gm_vec = Tensor("GM")
            with Core("aic0") as aic0:
                # GM->L1->L0B
                l1_x = Tensor("L1")
                l1_x.load(gm_x)
                x = Tensor("L0A")
                wait_flag("PIPE-MTE2", "PIPE-MTE1", 2)
                x.load(l1_x)
                # GM->L1->L0B
                l1_y = Tensor("L1")
                l1_y.load(gm_y)
                y = Tensor("L0B")  # L0B
                y.load(l1_y)
                set_flag("PIPE-MTE2", "PIPE-MTE1", 2)
                # L0C
                b = Tensor("L0C", "FP32", [128, 512], format="NC1HWC0")
                # mmad
                out = mmad(x, y, b, True)()
                gm_out.load(out[0])
                set_flag("aic0_PIPE-FIX", "aiv0_PIPE-MTE2", 1)
            with Core("aiv0") as aiv0:
                # 定义和分配UB上的变量
                x = Tensor("UB")
                y = Tensor("UB")
                z = Tensor("UB")

                # 将GM上的数据移动到UB对应内存空间上
                wait_flag("aic0_PIPE-FIX", "aiv0_PIPE-MTE2", 1)
                x.load(gm_z)
                y.load(gm_out)

                # 当前数据已加载到UB上，调用指令进行计算，结果保存在UB上
                out = vadd(x, y, z)()

                # 将UB上的数据移动到GM变量gm_z的地址空间上
                gm_vec.load(out[0])
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        with open(trace_file) as f:
            trace = json.load(f)
            self.assertIsNotNone(trace.get("traceEvents"))
            self.assertGreater(len(trace.get("traceEvents")), 0)
            gm_to_l1_end = 0
            l1_to_l0a_start = 0

            gm_to_ub_end = 0
            vadd_start = 0
            for event in trace.get("traceEvents"):
                self.assertIsNotNone(event.get("name"))
                self.assertIsNotNone(event.get("args"))
                if event.get("name") == "MOV-GM_TO_L1":
                    gm_to_l1_end = float(event.get("ts")) + float(event.get("dur"))
                if event.get("name") == "MOV-L1_TO_L0A":
                    l1_to_l0a_start = float(event.get("ts"))
                if event.get("name") == "MOV-GM_TO_UB":
                    gm_to_ub_end = float(event.get("ts")) + float(event.get("dur"))
                if event.get("name") == "VADD":
                    vadd_start = float(event.get("ts"))
            self.assertGreater(l1_to_l0a_start, gm_to_l1_end)
            self.assertGreaterEqual(vadd_start, gm_to_ub_end)
        self.clean()


if __name__ == '__main__':
    unittest.main()
