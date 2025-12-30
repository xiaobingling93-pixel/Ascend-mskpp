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
from mskpp import vshr, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_INT16_TYPE = "INT16"
FP_INT32_TYPE = "INT32"
FP_UINT16_TYPE = "UINT16"
FP_UINT32_TYPE = "UINT32"
FORMAT_TYPE = "ND"


def my_vshr(gm_x):
    ub_x = Tensor(UB_MEM)
    ub_y = Tensor(UB_MEM)
    ub_x.load(gm_x)
    out = vshr(ub_x, ub_y)()
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vshr_normal(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor(GM_MEM, FP_INT16_TYPE, [32, 64], format=FORMAT_TYPE)
            in_y = Tensor(GM_MEM, FP_INT16_TYPE, [32, 64], format=FORMAT_TYPE)
            in_x_int32 = Tensor(GM_MEM, FP_INT32_TYPE, [32, 64], format=FORMAT_TYPE)
            in_y_int32 = Tensor(GM_MEM, FP_INT32_TYPE, [32, 64], format=FORMAT_TYPE)
            in_x_uint16 = Tensor(GM_MEM, FP_UINT16_TYPE, [32, 64], format=FORMAT_TYPE)
            in_y_uint16 = Tensor(GM_MEM, FP_UINT16_TYPE, [32, 64], format=FORMAT_TYPE)
            in_x_uint32 = Tensor(GM_MEM, FP_UINT32_TYPE, [32, 64], format=FORMAT_TYPE)
            in_y_uint32 = Tensor(GM_MEM, FP_UINT32_TYPE, [32, 64], format=FORMAT_TYPE)
            out_y = my_vshr(in_x)
            out_y_int32 = my_vshr(in_x_int32)
            out_y_uint16 = my_vshr(in_x_uint16)
            out_y_uint32 = my_vshr(in_x_uint32)
            in_y.load(out_y)
            in_y_int32.load(out_y_int32)
            in_y_uint16.load(out_y_uint16)
            in_y_uint32.load(out_y_uint32)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()