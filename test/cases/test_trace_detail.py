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

import json
import os
import unittest

from mskpp import mmad, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase
 
def dsl_mmad(gm_x, gm_y, gm_z):
    l1_x = Tensor("L1")
    l1_y = Tensor("L1")
    l1_x.load(gm_x)
    l1_y.load(gm_y)
    x = Tensor("L0A")
    y = Tensor("L0B")
    x.load(l1_x)
    y.load(l1_y)
    z = Tensor("L0C", "FP32", [32, 16], format="NC1HWC0")
    out = mmad(x, y, z, True)() # 对于输出需要返回传出
    z = out[0]
    return z
 
 
class TestUtilsMethods(TestBase):
    TRACE_FILE = "trace.json"
 
    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')
            
    def test_trace_detail(self):
        with Chip("Ascend910B3") as chip:
            chip.enable_trace()
            for _ in range(1):
                in_x = Tensor("GM", "FP16", [32, 48], format="ND")
                in_y = Tensor("GM", "FP16", [48, 16], format="ND")
                in_z = Tensor("GM", "FP32", [32, 16], format="NC1HWC0")
                out_z = dsl_mmad(in_x, in_y, in_z)
                in_z.load(out_z)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        with open(trace_file) as f:
            trace = json.load(f)
            self.assertIsNotNone(trace.get("traceEvents"))
            self.assertGreater(len(trace.get("traceEvents")), 0)
            for event in trace.get("traceEvents"):
                self.assertIsNotNone(event.get("name"))
                self.assertIsNotNone(event.get("args"))
                if event.get("name") == "MMAD":
                    self.assertEqual(tuple(event.get("args").keys()), ("Cycle", "Task Type", "Ops", "Ops/Cycle"))
                elif event.get("ph") == 'X':
                    self.assertEqual(tuple(event.get("args").keys()), ("Cycle", "Size(B)", "Bandwidth(GB/s)"))
        self.clean()

if __name__ == '__main__':
    unittest.main()