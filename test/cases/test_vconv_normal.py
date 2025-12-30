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
from mskpp import vconv, Tensor, Chip
from mskpp._C import task_schedule
from test.utils.test_base import TestBase


def my_vconv(gm_x, dtype):
    ub_x = Tensor("UB")
    ub_y = Tensor("UB")
    ub_x.load(gm_x)
    out = vconv(ub_x, ub_y, dtype)()
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    TRACE_FILE = 'trace.json'

    def clean(self):
        task_schedule.Schedule().clean()
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_vconv_normal_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "FP16", [8, 2048], format="ND")
            in_y = Tensor("GM", "FP32", [8, 2048], format="ND")
            out_y = my_vconv(in_x, "FP32")
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vconv_fp162s4_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "FP16", [8, 2048], format="ND")
            in_y = Tensor("GM", "INT4", [8, 2048], format="ND")
            out_y = my_vconv(in_x, "INT4")
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vconv_fp162s8_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "FP16", [8, 2048], format="ND")
            in_y = Tensor("GM", "INT8", [8, 2048], format="ND")
            out_y = my_vconv(in_x, "INT8")
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vconv_fp162u8_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "FP16", [8, 2048], format="ND")
            in_y = Tensor("GM", "UINT8", [8, 2048], format="ND")
            out_y = my_vconv(in_x, "UINT8")
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vconv_s42fp16_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "INT4", [8, 2048], format="ND")
            in_y = Tensor("GM", "FP16", [8, 2048], format="ND")
            out_y = my_vconv(in_x, "FP16")
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()

    def test_vconv_bf162fp32_expect_trace_successful_create(self):
        with Chip("Ascend910B1") as chip:
            chip.enable_trace()
            in_x = Tensor("GM", "BF16", [8, 2048], format="ND")
            in_y = Tensor("GM", "FP32", [8, 2048], format="ND")
            out_y = my_vconv(in_x, "FP32")
            in_y.load(out_y)
            trace_file = os.path.join(chip.output_dir, self.TRACE_FILE)
        self.assertTrue(os.path.exists(trace_file))
        self.clean()


if __name__ == '__main__':
    unittest.main()
