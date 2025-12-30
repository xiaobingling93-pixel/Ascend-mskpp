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
import stat
import unittest

from unittest import mock
from mskpp import mmad, Tensor, Chip
from test.utils.test_base import TestBase


PROF_LINES = [
    "Model ID,Task ID,Stream ID,Op Name,OP Type,Task Type,Task Start Time,Task Duration(us),Task Wait Time(us),\
Block Dim,Input Shapes,Input Data Types,Input Formats,Output Shapes,Output Data Types,Output Formats,\
aicore_time(us),total_cycles,vec_time(us),vec_ratio,mac_time(us),mac_ratio,scalar_time(us),scalar_ratio,\
mte1_time(us),mte1_ratio,mte2_time(us),mte2_ratio,mte3_time(us),mte3_ratio,icache_miss_rate,memory_bound",
    "4294967295,1,47,add_custom,add_custom,AI_CORE,1043640017380.831,82.11,0,8,N/A,N/A,N/A,N/A,N/A,N/A,9.87,\
78923,0.2261,0.0229,0,0,8.8732,0.899,0,0,3.8364,0.3887,2.4525,0.2485,0.0002,16.9677"
]


class MockCSV:

    @classmethod
    def reader(cls):
        for line in PROF_LINES:
            yield line

    @classmethod
    def dict_reader(cls):
        heads = PROF_LINES[0].split(",")
        values = PROF_LINES[1].split(",")
        return [{head: values[i] for i, head in enumerate(heads)}]


def dsl_mmad(gm_x, gm_y, gm_z):
    l1_x = Tensor("L1")
    l1_y = Tensor("L1")
    l1_x.load(gm_x)
    l1_y.load(gm_y)
    x = Tensor("L0A")
    y = Tensor("L0B")
    x.load(l1_x)
    y.load(l1_y)
    z = Tensor("L0C", "FP32", [32, 16], format="NC1HWC0")
    out = mmad(x, y, z, True)()  # 对于输出需要返回传出
    z = out[0]
    return z


class TestUtilsMethods(TestBase):
    STATISTIC_CSV_FILES = ["Pipe_statistic.csv", "Instruction_statistic.csv"]
    HTML_FILES = ["instruction_cycle_consumption.html"]

    def clean(self):
        work_dir = os.getcwd()
        self.batch_delete_folders(work_dir, 'MSKPP_*')

    def test_check_statistic_csv_file(self):
        with mock.patch('sys.stdout.write', lambda x: None):
            with Chip("Ascend910B3") as chip:
                chip.enable_metrics()
                for _ in range(1):
                    in_x = Tensor("GM", "FP16", [32, 48], format="ND")
                    in_y = Tensor("GM", "FP16", [48, 16], format="ND")
                    in_z = Tensor("GM", "FP32", [32, 16], format="NC1HWC0")
                    out_z = dsl_mmad(in_x, in_y, in_z)
                    in_z.load(out_z)
                    output_dir = chip.output_dir

        for path in self.STATISTIC_CSV_FILES:
            file_path = os.path.join(output_dir, path)
            self.assertTrue(os.path.exists(file_path))
            modes = stat.S_IWUSR | stat.S_IRUSR | stat.S_IFREG
            self.assertEqual(os.stat(file_path).st_mode, modes)
        pipe_file = os.path.join(output_dir, "Pipe_statistic.csv")
        with open(pipe_file) as f:
            lines = f.readlines()
            self.assertEqual(
                lines[0], '"Pipe","Duration(us)","Cycle","Size(B)","Ops"\n')
            self.assertEqual(len(lines), 6)
        instr_file = os.path.join(output_dir, "Instruction_statistic.csv")
        with open(instr_file) as f:
            lines = f.readlines()
            self.assertEqual(
                lines[0], '"Instruction","Duration(us)","Cycle","Size(B)","Ops"\n')
            self.assertEqual(len(lines), 6)

    def test_check_prof_summary_path(self):
        with self.assertRaises(Exception):
            with Chip("Ascend910B1") as chip:
                chip.set_prof_summary_path("not_found.csv")

    def test_parse_prof_summary(self):
        from mskpp.core.metric.metrics_summary import ProfSummary
        with mock.patch("csv.reader", return_value=MockCSV.reader()):
            with mock.patch("csv.DictReader", return_value=MockCSV.dict_reader()):
                with mock.patch("mskpp.core.metric.file_system.FileChecker.check_input_file", return_value=True):
                    prof_summary = ProfSummary().parse(__file__)
        golden_prof = {
            0: {
                'Total': 9.87,
                'PIPE-V': 0.2261,
                'PIPE-MTE2': 3.8364,
                'PIPE-MTE3': 2.4525
            }
        }
        self.assertCountEqual(prof_summary, golden_prof)

    def test_pipe_metrics_summary_output(self):
        from collections import OrderedDict
        from mskpp.core.metric.metrics_summary import PipeMetricsSummary
        pipe_metrics_summary = PipeMetricsSummary()
        mock_pipe_summary = OrderedDict(
            [
                ('Total', OrderedDict(
                    [
                        ('Duration(us)', 1.0089)
                    ]
                )),
                ('PIPE-MTE2', OrderedDict(
                    [
                        ('Duration(us)', 0.5411)
                    ]
                ))
            ]
        )
        golden_pipe_summary = OrderedDict(
            [
                ('Total', OrderedDict(
                    [
                        ('Duration(us)', 1.0089),
                        ('ProfDuration(us)_0', 9.87),
                        ('ProfRatio_0', 9.7829)
                    ]
                )),
                ('PIPE-MTE2', OrderedDict(
                    [
                        ('Duration(us)', 0.5411),
                        ('ProfDuration(us)_0', 3.8364),
                        ('ProfRatio_0', 7.09)
                    ]
                ))
            ]
        )

        with mock.patch.object(pipe_metrics_summary, "_summary", mock_pipe_summary):
            with mock.patch("csv.reader", return_value=MockCSV.reader()):
                with mock.patch("csv.DictReader", return_value=MockCSV.dict_reader()):
                    os.chmod(__file__, 0o640)
                    PipeMetricsSummary().set_prof_summary_path(__file__)
                    PipeMetricsSummary().add_prof_summary()
                    self.assertDictEqual(
                        PipeMetricsSummary().get_summary(), golden_pipe_summary)


if __name__ == '__main__':
    unittest.main()
