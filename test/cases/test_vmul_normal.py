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
from mskpp import vmul, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase
 
 
def my_vmul(gm_x, gm_y, gm_z):
    ub_x, ub_y, ub_z = Tensor("UB"), Tensor("UB"), Tensor("UB")
    ub_x.load(gm_x)
    ub_y.load(gm_y)
    out = vmul(ub_x, ub_y, ub_z)()
    return out[0]


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vmul_normal(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            for _ in range(1):
                in_x = Tensor("GM", "FP16", [32, 48], format="ND")
                in_y = Tensor("GM", "FP16", [32, 48], format="ND")
                in_z = Tensor("GM", "FP16", [32, 48], format="ND")
                out_z = my_vmul(in_x, in_y, in_z)
                in_z.load(out_z)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()
