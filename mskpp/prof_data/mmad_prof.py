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

from math import ceil
from mskpp.core.prof_data import PrefModel, ProfDataRegister
from mskpp._C import prof_data, arch
from mskpp.core.common import checker


@ProfDataRegister.register("MMAD")
class MmadPref(PrefModel):
    def __init__(self, inputs, outputs):
        super(MmadPref, self).__init__("MMAD", inputs, outputs)

    def size(self):
        x, y, b = self.inputs
        if len(x.size) < 2 or len(y.size) < 2:
            raise Exception("The dim of shape is invalid for mmad")
        tile_m = x.size[0]
        tile_k = x.size[1]
        tile_n = y.size[1]
        return tile_m * tile_k * tile_n

    def time(self):
        x, y, b = self.inputs
        granularity = self.size()
        if not checker.check_convert_long_size(granularity):
            raise Exception("The shape size is too large for mmad")
        real_perf = prof_data.MmadData().get(granularity, x.dtype)
        if real_perf <= 0:
            raise Exception("Cannot get running time of {}".format(self.name))
        cycles = ceil(arch.get_size_of(x.dtype) * granularity / real_perf)
        return cycles

    def pipe_name(self):
        from mskpp.core.aicore import Core
        return Core.get_aicore_pipe_name("PIPE-M")
