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

from mskpp.core.common import checker


class TestChecker(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_required_type_with_string_expect_string(self):
        test_param = "string"
        self.assertTrue(checker.is_required_type(test_param, str))

    def test_is_required_type_with_string_expect_bool(self):
        test_param = "string"
        self.assertFalse(checker.is_required_type(test_param, bool))

    def test_is_required_type_with_float_expect_int(self):
        test_param = 1.0
        self.assertFalse(checker.is_required_type(test_param, int))

    def test_is_mem_type_valid_expect_success(self):
        test_param = "GM"
        self.assertTrue(checker.is_mem_type_valid(test_param))

    def test_is_mem_type_valid_expect_failed(self):
        test_param = "Ub"
        self.assertFalse(checker.is_mem_type_valid(test_param))

    def test_is_dtype_valid_with_full_type_expect_success(self):
        test_param = "INT8"
        self.assertTrue(checker.is_dtype_valid(test_param, 0))

    def test_is_dtype_valid_with_full_type_expect_failed(self):
        test_param = "BF8"
        self.assertFalse(checker.is_dtype_valid(test_param, 0))

    def test_is_dtype_valid_with_basic_type_expect_success(self):
        test_param = "INT16"
        self.assertTrue(checker.is_dtype_valid(test_param, 1))

    def test_is_dtype_valid_with_basic_type_expect_failed(self):
        test_param = "INT8"
        self.assertFalse(checker.is_dtype_valid(test_param, 1))

    def test_is_format_valid_with_valid_format_expect_success(self):
        test_param = "NCHW"
        self.assertTrue(checker.is_format_valid(test_param))

    def test_is_format_valid_with_wrong_format_expect_failed(self):
        test_param = "NC0HWC1"
        self.assertFalse(checker.is_format_valid(test_param))

    def test_is_gm_type_valid_with_valid_type_expect_success(self):
        test_param = "HBM"
        self.assertTrue(checker.is_gm_type_valid(test_param))

    def test_is_gm_type_valid_with_wrong_type_expect_failed(self):
        test_param = "L1Cache"
        self.assertFalse(checker.is_gm_type_valid(test_param))
