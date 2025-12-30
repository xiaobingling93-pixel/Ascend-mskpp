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
from mskpp import Tensor
from mskpp._C import task_schedule
from test.utils.test_base import TestBase


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_tensor_slice_normal(self):
        in_x = Tensor("GM", "FP16", [32, 48], format="ND")
        in_x2 = in_x[:]
        self.assertEqual(in_x.size, in_x2.size)

    def test_tensor_slice_abnormal(self):
        in_x = Tensor("GM", "FP16", [32, 48], format="ND")
        try:
            in_x[1, ...]
        except TypeError as error:
            self.assertEqual(type(error), TypeError)


if __name__ == '__main__':
    unittest.main()
