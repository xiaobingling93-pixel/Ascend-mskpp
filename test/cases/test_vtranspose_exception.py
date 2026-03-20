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
from mskpp import vtranspose, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase


def my_vtranspose(gm_x, gm_y):
    ub_x, ub_y = Tensor("UB"), Tensor("UB")
    ub_x.load(gm_x)
    out = vtranspose(ub_x, ub_y)()
    return out[0]


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vtranspose_normal(self):
        in_x = Tensor("GM", "FP16", [16, 16], format="ND")
        in_y = Tensor("GM", "FP16", [16, 16], format="ND")
        _ = my_vtranspose(in_x, in_y)
        self.clean()

    def test_vtranspose_abnormal(self):
        in_x = Tensor("GM", "FP16", [16, 32], format="ND")
        in_y = Tensor("GM", "FP16", [32, 16], format="ND")
        self.assertRaises(ValueError, my_vtranspose, in_x, in_y)
        self.clean()


if __name__ == '__main__':
    unittest.main()