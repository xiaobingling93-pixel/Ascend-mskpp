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
from mskpp import vdiv, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_16_TYPE = "FP16"
FP_32_TYPE = "FP32"
FORMAT_TYPE = "ND"


def my_vdiv(gm_x, gm_y, gm_z):
    ub_x, ub_y, ub_z = Tensor(UB_MEM), Tensor(UB_MEM), Tensor(UB_MEM)
    ub_x.load(gm_x)
    ub_y.load(gm_y)
    out = vdiv(ub_x, ub_y, ub_z)()
    return out[0]


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vdiv_normal(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            for _ in range(1):
                in_x = Tensor(GM_MEM, FP_16_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_y = Tensor(GM_MEM, FP_16_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_z = Tensor(GM_MEM, FP_16_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_x_fp32 = Tensor(GM_MEM, FP_32_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_y_fp32 = Tensor(GM_MEM, FP_32_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_z_fp32 = Tensor(GM_MEM, FP_32_TYPE, [8, 2048], format=FORMAT_TYPE)
                out_z = my_vdiv(in_x, in_y, in_z)
                out_z_fp32 = my_vdiv(in_x_fp32, in_y_fp32, in_z_fp32)
                in_z.load(out_z)
                in_z_fp32.load(out_z_fp32)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()
