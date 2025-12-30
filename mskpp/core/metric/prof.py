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

import csv
from mskpp.utils import logger
from .file_system import FileChecker
from ..common.singleton import Singleton


@Singleton
class ProfSummary:
    pipe_map = {
        "aicore_time(us)": "Total",
        "aic_mac_time(us)": "PIPE-M",
        "aic_mte1_time(us)": "PIPE-MTE1",
        "aic_mte2_time(us)": "PIPE-MTE2",
        "aic_fixpipe_time(us)": "PIPE-FIX",
        "aiv_time(us)": "Total",
        "aiv_vec_time(us)": "PIPE-V",
        "aiv_mte2_time(us)": "PIPE-MTE2",
        "aiv_mte3_time(us)": "PIPE-MTE3",
        "mac_time(us)": "PIPE-M",
        "mte1_time(us)": "PIPE-MTE1",
        "mte2_time(us)": "PIPE-MTE2",
        "mte3_time(us)": "PIPE-MTE3",
        "fixpipe_time(us)": "PIPE-FIX",
        "vec_time(us)": "PIPE-V",
    }

    def __init__(self):
        self._summary = {}

    @staticmethod
    def _check_can_transfer_float(value):
        try:
            float(value)
        except ValueError:
            return False
        return True

    def prof_summary_clear(self):
        self.__init__()

    def parse(self, prof_summary_path):
        file_checker = FileChecker(prof_summary_path, "csv")
        if not file_checker.check_input_file():
            logger.error("Profiling Summary file check fail")
            return self._summary
        with open(prof_summary_path, "r", encoding="utf-8") as fd:
            reader = csv.reader(fd)
            try:
                head = next(reader)
            except StopIteration as ex:
                logger.error(f"{prof_summary_path} is empty")
                return self._summary
            fd.seek(0)
            self._parse_csv(csv.DictReader(fd))
        return self._summary

    def _parse_csv(self, csv_reader):
        for index, row in enumerate(csv_reader):
            if not self._check_row(row):
                continue
            self._summary[index] = {}
            for k, v in row.items():
                if self._check_cell(k, v):
                    pipe_name = self.pipe_map.get(k, "")
                    self._summary[index].setdefault(pipe_name, 0)
                    self._summary[index][pipe_name] += float(v)

    def _check_cell(self, key, content):
        if key not in self.pipe_map:
            return False
        if content in ["0", "N/A", "UNKNOWN", "", None]:
            return False
        return self._check_can_transfer_float(content)

    def _check_row(self, row):
        return any([self._check_cell(k, row.get(k)) for k in self.pipe_map])