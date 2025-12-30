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
from test.utils.test_base import TestBase
from mskpp import Tensor, Chip

NHWC_MEM = "NHWC"


class TestCopy(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_expect_fb_bt_start_after_mov_l1(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            gm2l1_end = 0
            for _ in range(2):
                in_x = Tensor("GM", "FP16", [64], format="ND")
                l1_x = Tensor("L1")
                fp_x = Tensor("FB")
                bt_x = Tensor("BT")
                l1_x.load(in_x)
                l1_x_to_fp = l1_x[0:32]
                l1_x_to_bt = l1_x[32:64]
                fp_x.load(l1_x_to_fp)
                bt_x.load(l1_x_to_bt)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)

        with open(trace_file) as f:
            trace_contents = json.load(f)

        for content in trace_contents.get("traceEvents"):
            if content.get("name") == "MOV-GM_TO_L1":
                gm2l1_end = content.get("ts") + content.get("dur")
            if content.get("name") == "MOV-L1_TO_FB":
                l12fp_start = content.get("ts")
                self.assertAlmostEqual(gm2l1_end, l12fp_start)
            if content.get("name") == "MOV-L1_TO_BT":
                l12bt_start = content.get("ts")
                self.assertAlmostEqual(gm2l1_end, l12bt_start)
        self.clean()

    def test_move_gm2l1_nd2nz_expect_tensor_format_trans_keep(self):
        with Chip("Ascend910B1"):
            for _ in range(2):
                in_x = Tensor("GM", "FP16", [128, 256], format="ND")
                l1_x1 = Tensor("L1", format="NZ")
                l1_x2 = Tensor("L1", format="NZ")
                l1_x1.load(in_x[127, 0:128])
                l1_x2.load(in_x[127, 128:])
                self.assertEqual(l1_x1.format, "NZ")
                self.assertEqual(l1_x2.format, "NZ")
        self.clean()

    def test_move_l0c2gm_nz2nd_expect_tensor_format_trans_keep(self):
        with Chip("Ascend910B1"):
            for _ in range(2):
                l0cout_x = Tensor("L0C", "FP16", [128, 256], format="NC1HWC0", is_inited=True)
                gm_x1 = Tensor("GM", format=NHWC_MEM)
                gm_x2 = Tensor("GM", format=NHWC_MEM)
                gm_x1.load(l0cout_x[127, 0:128])
                gm_x2.load(l0cout_x[127, 128:])
                self.assertEqual(gm_x1.format, NHWC_MEM)
                self.assertEqual(gm_x2.format, NHWC_MEM)
        self.clean()


if __name__ == '__main__':
    unittest.main()