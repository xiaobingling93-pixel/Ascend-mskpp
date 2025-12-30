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
from mskpp import vbitsort, vmrgsort, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase

UB_MEM = "UB"
GM_MEM = "GM"
FP_16_TYPE = "FP16"
UINT32_TYPE = "UINT32"
UINT64_TYPE = "UINT64"
FORMAT_TYPE = "ND"


def my_vbitsort(gm_x, gm_y, gm_z):
    x = Tensor(UB_MEM)
    y = Tensor(UB_MEM)
    z = Tensor(UB_MEM)

    x.load(gm_x)
    y.load(gm_y)

    out = vbitsort(x, y, z)()
    gm_z.load(out[0])


def my_vmrgsort4(gm_x, gm_y, gm_z):
    x = Tensor(UB_MEM)
    y = Tensor(UB_MEM)
    z = Tensor(UB_MEM)

    x.load(gm_x)
    y.load(gm_y)

    out = vmrgsort(x, y, z)()
    gm_z.load(out[0])


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vbitsort_normal(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            for _ in range(1):
                in_x = Tensor(GM_MEM, FP_16_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_y = Tensor(GM_MEM, UINT32_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_z = Tensor(GM_MEM, FP_16_TYPE, [16, 4096], format=FORMAT_TYPE)
                my_vbitsort(in_x, in_y, in_z)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vmrgsort4_normal(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            for _ in range(1):
                in_x = Tensor(GM_MEM, FP_16_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_y = Tensor(GM_MEM, UINT64_TYPE, [8, 2048], format=FORMAT_TYPE)
                in_z = Tensor(GM_MEM, FP_16_TYPE, [8, 2048], format=FORMAT_TYPE)
                my_vmrgsort4(in_x, in_y, in_z)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()