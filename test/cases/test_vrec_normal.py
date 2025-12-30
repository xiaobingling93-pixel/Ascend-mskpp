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
from mskpp import vrec, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase


def my_vrec(gm_x):
    ub_x = Tensor("UB")
    ub_y = Tensor("UB")
    ub_x.load(gm_x)
    out = vrec(ub_x, ub_y)()
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vrec_normal_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "FP16", [256, 64], format="ND")
            in_y = Tensor("GM", "FP16", [256, 64], format="ND")
            out_y = my_vrec(in_x)
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()
