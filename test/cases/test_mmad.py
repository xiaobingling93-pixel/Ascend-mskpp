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
from mskpp import mmad, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

FORMAT_TYPE_ND = "ND"
FORMAT_TYPE_NZ = "NZ"
FORMAT_TYPE_NC1HWC0 = "NC1HWC0"


def l0a_slice_mmad(gm_x, gm_y, gm_z):
    l1_x1 = Tensor("L1")
    l1_x2 = Tensor("L1")
    l1_y = Tensor("L1")
    l1_x1.load(gm_x[0:16, :])
    l1_x2.load(gm_x[16:32, :])
    l1_y.load(gm_y)
    x1 = Tensor("L0A")
    x2 = Tensor("L0A")
    y = Tensor("L0B")
    x1.load(l1_x1)
    x2.load(l1_x2)
    y.load(l1_y)
    z = Tensor("L0C", "FP32", [16, 16], format=FORMAT_TYPE_NC1HWC0)
    out1 = mmad(x1, y, z, True)()
    out2 = mmad(x2, y, z, True)()
    z1 = out1[0]
    z2 = out2[0]
    return z1, z2


def mmad_with_bias(gm_x, gm_y, gm_z, is_inited=False):
    l1_x = Tensor("L1", format=FORMAT_TYPE_NZ)
    l1_y = Tensor("L1", format=FORMAT_TYPE_NZ)
    l1_bias = Tensor("L1")
    bias = Tensor("BT")
    l1_x.load(gm_x)
    l1_y.load(gm_y)
    l1_bias.load(gm_z)
    x = Tensor("L0A")
    y = Tensor("L0B")
    x.load(l1_x)
    y.load(l1_y)
    bias.load(l1_bias)
    out = mmad(x, y, bias, is_inited)()

    z = out[0]
    return z


class TestDifferentMmad(TestBase):
    TRACE_FILE = 'trace.json'
    HTML_FILE = 'instruction_cycle_consumption.html'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_tensor_slice_mmad(self):
        # The first L1-TO-L0A EVENT should be the start from the end of first GM-TO-L1
        # The second L1-TO-L0A EVENT should be the start from the end of second GM-TO-L1
        l12l0a_start = 0
        gm2l1_end = 1
        with Chip("Ascend910B3") as chip:
            chip.enable_trace()
            chip.enable_metrics()
            for _ in range(2):
                in_x = Tensor("GM", "FP16", [32, 48], format="ND")
                in_y = Tensor("GM", "FP16", [48, 16], format="ND")
                in_z = Tensor("GM", "FP32", [32, 16], format="NC1HWC0")
                out_z1, out_z2 = l0a_slice_mmad(in_x, in_y, in_z)
                in_z.load(out_z1)
                in_z.load(out_z2)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_mmad_with_bias_expect_out_format_nz(self):
        with Chip("Ascend910B1"):
            for _ in range(2):
                in_x = Tensor("GM", "FP16", [32, 64], format=FORMAT_TYPE_ND)
                in_y = Tensor("GM", "FP16", [64, 48], format=FORMAT_TYPE_ND)
                bias = Tensor("GM", "FP32", [48], format=FORMAT_TYPE_ND)
                in_z = Tensor("GM", "FP32", [32, 48], format=FORMAT_TYPE_ND)
                out_z = mmad_with_bias(in_x, in_y, bias)
                self.assertEqual(out_z.format, FORMAT_TYPE_NZ)
                in_z.load(out_z)
        self.clean()

    def test_mmad_with_invalid_param_expect_failed(self):
        with self.assertRaises(Exception):
            with Chip("Ascend910B1"):
                in_x = Tensor("GM", "FP16", [3285, 6465], format=FORMAT_TYPE_ND)
                in_y = Tensor("GM", "FP16", [6465, 4894], format=FORMAT_TYPE_ND)
                bias = Tensor("GM", "FP32", [4894], format=FORMAT_TYPE_ND)
                in_z = Tensor("GM", "FP32", [3285, 4894], format=FORMAT_TYPE_ND)
                out_z = mmad_with_bias(in_x, in_y, bias, 1)
                in_z.load(out_z)
        self.clean()


if __name__ == '__main__':
    unittest.main()