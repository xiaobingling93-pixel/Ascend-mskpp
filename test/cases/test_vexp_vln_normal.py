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
from mskpp import vexp, vln, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_16_TYPE = "FP16"
FP_32_TYPE = "FP32"
FORMAT_TYPE = "ND"


def my_vexp(gm_x, gm_y):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vexp(ub_x, ub_y)()
    z = out[0]
    return z


def my_vln(gm_x, gm_y):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vln(ub_x, ub_y)()
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vexp_vln_normal_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor(GM_MEM, FP_16_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y = Tensor(GM_MEM, FP_16_TYPE, [8, 2048], format=FORMAT_TYPE)
            in_x_fp32 = Tensor(GM_MEM, FP_32_TYPE, [4, 2048], format=FORMAT_TYPE)
            in_y_fp32 = Tensor(GM_MEM, FP_32_TYPE, [8, 2048], format=FORMAT_TYPE)
            out_y1 = my_vexp(in_x, in_y[0:4, :])
            out_y2 = my_vln(in_x, in_y[4:8, :])
            out_y1_fp32 = my_vexp(in_x_fp32, in_y_fp32[0:4, :])
            out_y2_fp32 = my_vln(in_x_fp32, in_y_fp32[4:8, :])
            in_y.load(out_y1)
            in_y.load(out_y2)
            in_y_fp32.load(out_y1_fp32)
            in_y_fp32.load(out_y2_fp32)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()
