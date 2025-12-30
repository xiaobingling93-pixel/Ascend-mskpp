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
from mskpp import vcadd, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase


def my_vcadd(gm_x, gm_y, reduce_num):
    ub_x = Tensor("UB")
    ub_y = Tensor("UB")
    ub_z = Tensor("UB")
    ub_x.load(gm_x)
    out = vcadd(ub_x, ub_y, reduce_num)()
    out = vcadd(out[0], ub_z, reduce_num)()
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vcadd_normal_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "FP16", [256, 64], format="ND")
            in_y = Tensor("GM", "FP16", [32], format="ND")
            out_y = my_vcadd(in_x, in_y, 64)
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vcadd_invalid_reduce_num_expect_failed(self):
        with self.assertRaises(Exception):
            with Chip("Ascend910B1") as chip:
                chip.enable_trace()
                in_x = Tensor("GM", "FP16", [256, 64], format="ND")
                in_y = Tensor("GM", "FP16", [32], format="ND")
                out_y = my_vcadd(in_x, in_y, True)
                in_y.load(out_y)
        self.clean()

    def test_vcadd_invalid_tnesor_expect_failed(self):
        with self.assertRaises(Exception):
            with Chip("Ascend910B1") as chip:
                chip.enable_trace()
                in_x = 1
                in_y = Tensor("GM", "FP16", [32], format="ND")
                out_y = my_vcadd(in_x, in_y, 64)
                in_y.load(out_y)
        self.clean()


if __name__ == '__main__':
    unittest.main()
