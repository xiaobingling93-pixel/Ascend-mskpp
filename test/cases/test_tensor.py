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

from mskpp import Tensor


class TestTensor(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simplify_tensor_build_expect_success(self):
        success_tensor_build_flag = True
        try:
            Tensor("UB")
            Tensor("L0A")
            Tensor("FB")
        except Exception:
            success_tensor_build_flag = False
        self.assertTrue(success_tensor_build_flag)

    def test_simplify_tensor_build_expect_failed(self):
        with self.assertRaises(Exception):
            Tensor("TN")

    def test_normal_tensor_build_expect_success(self):
        success_tensor_build_flag = True
        try:
            Tensor("UB", "FP16", [10, 20], format="ND")
            Tensor("GM", "FP32", [1, 20])
            Tensor("FB", "UINT2", is_inited=True)
        except Exception:
            success_tensor_build_flag = False
        self.assertTrue(success_tensor_build_flag)

    def test_normal_tensor_build_expect_failed(self):
        with self.assertRaises(Exception):
            Tensor("TN")

    def test_abnormal_tensor_with_big_size_expect_failed(self):
        with self.assertRaises(Exception):
            Tensor("UB", "FP16", [1, 2 ** 31], format="ND")

    def test_tensor_load_with_wrong_set_value_expect_failed(self):
        with self.assertRaises(Exception):
            gm = Tensor("GM", "FP32", [1, 893298238923802389324])
            ub = Tensor("UB")
            ub.load(gm, set_value="test")

    def test_tensor_load_with_wrong_expect_value_expect_failed(self):
        with self.assertRaises(Exception):
            gm = Tensor("GM", "FP32", [1, 893298238923802389324])
            ub = Tensor("UB")
            ub.load(gm, set_value=1, expect_value=True)

    def test_tensor_load_with_wrong_repeat_expect_failed(self):
        with self.assertRaises(Exception):
            gm = Tensor("GM", "FP32", [1, 893298238923802389324])
            ub = Tensor("UB")
            ub.load(gm, repeat=True)

    def test_tensor_load_with_load_empty_dtype_expect_failed(self):
        with self.assertRaises(Exception):
            gm = Tensor("L0A", [1, 893298238923802389324])
            ub = Tensor("UB")
            ub.load(gm)

    def test_tensor_get_item_slice(self):
        gm = Tensor("GM", "FP32", [128, 256], format="ND")
        gm_split = gm[1:5]
        self.assertEqual(gm_split.size, [4, 256])

    def test_tensor_get_item_tuple_slice(self):
        gm = Tensor("GM", "FP32", [128, 256], format="ND")
        gm_split = gm[1:5, ::10]
        self.assertEqual(gm_split.size, [4, 26])

    def test_tensor_get_item_tuple_int(self):
        gm = Tensor("GM", "FP32", [128, 256], format="ND")
        gm_split = gm[5,]
        self.assertEqual(gm_split.size, [256])

    def test_tensor_get_item_type_error(self):
        with self.assertRaises(TypeError):
            gm = Tensor("GM", "FP32", [128, 256], format="ND")
            gm_split = gm["test"]

    def test_tensor_get_item_slice_size_error(self):
        with self.assertRaises(Exception):
            gm = Tensor("GM", "FP32", [128, 256], format="ND")
            gm_split = gm[1, 2, 3]

    def test_tensor_get_item_tuple_int_key_error(self):
        with self.assertRaises(Exception):
            gm = Tensor("GM", "FP32", [128, 256], format="ND")
            gm_split = gm[128]