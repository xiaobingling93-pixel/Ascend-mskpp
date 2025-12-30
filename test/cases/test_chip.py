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

import unittest
import os
from mskpp import Chip
from test.utils.test_base import TestBase


class TestCopy(TestBase):
    TRACE_FILE = 'trace.json'
    HTML_FILE = 'instruction_cycle_consumption.html'

    def clean(self):
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_expect_exception_for_chip_name(self):
        with self.assertRaises(Exception):
            with Chip("Ascend910B20"):
                pass
        self.clean()

    def test_expect_exception_for_wrong_debug_mode(self):
        with self.assertRaises(Exception):
            with Chip("Ascend910B1", "debug_mode"):
                pass
        self.clean()
