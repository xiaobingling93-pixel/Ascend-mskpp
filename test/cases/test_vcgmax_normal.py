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
import os
import unittest
from mskpp import vcgmax, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_16_TYPE = "FP16"
FP_32_TYPE = "FP32"
FORMAT_TYPE = "ND"


def my_vcgmax(gm_x, gm_y, reduce_num):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vcgmax(ub_x, ub_y, reduce_num)()
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vcadd_normal_expect_trace_successful_create(self):
        in_x = Tensor(GM_MEM, FP_16_TYPE, [256, 64], format=FORMAT_TYPE)
        in_y = Tensor(GM_MEM, FP_16_TYPE, format=FORMAT_TYPE)
        in_x_fp32 = Tensor(GM_MEM, FP_32_TYPE, [256, 64], format=FORMAT_TYPE)
        in_y_fp32 = Tensor(GM_MEM, FP_32_TYPE, format=FORMAT_TYPE)
        out_y = my_vcgmax(in_x, in_y, 8)
        out_y_fp32 = my_vcgmax(in_x_fp32, in_y_fp32, 8)
        in_y.load(out_y)
        in_y_fp32.load(out_y_fp32)
        self.assertEqual(in_y.size[0], 256)
        self.assertEqual(in_y.size[1], 8)
        self.assertEqual(in_y_fp32.size[0], 256)
        self.assertEqual(in_y_fp32.size[1], 8)
        self.clean()

    def test_vcadd_with_invalid_reduce_num_expect_failed(self):
        with self.assertRaises(Exception):
            in_x = Tensor(GM_MEM, FP_16_TYPE, [256, 64], format=FORMAT_TYPE)
            in_y = Tensor(GM_MEM, FP_16_TYPE, format=FORMAT_TYPE)
            out_y = my_vcgmax(in_x, in_y, (8,))
            in_y.load(out_y)
        self.clean()


if __name__ == '__main__':
    unittest.main()
