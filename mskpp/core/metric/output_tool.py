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
import sys
import csv


SAVE_DATA_FILE_AUTHORITY = stat.S_IWUSR | stat.S_IRUSR
OPEN_FLAGS = os.O_WRONLY | os.O_CREAT


class TableOutputWrapper:
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.file = None
        self.stdout = None
        self.csv_writer = None

    def __enter__(self):
        if self.filepath:
            self.file = os.fdopen(os.open(self.filepath, OPEN_FLAGS, SAVE_DATA_FILE_AUTHORITY), 'w')
            self.file.truncate()
            self.csv_writer = csv.writer(self.file, quoting=csv.QUOTE_ALL)
        else:
            self.stdout = sys.stdout
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

    def write(self, row):
        if self.csv_writer:
            self.csv_writer.writerow(row)
        if self.stdout:
            fmt = "{:<20} " * len(row)
            self.stdout.write(fmt.format(*row))
            self.stdout.write("\n")