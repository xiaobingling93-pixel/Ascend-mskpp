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

from mskpp._C import arch
from .tensor import Tensor
from .chip import Chip
from .prof_data import PrefModel, ProfDataRegister
from .computation_instruction import ComputationInstruction
from .sync_instruction import set_flag, wait_flag
from .api_register import InstrApiRegister
from .aicore import Core
from .vec_scope import VecScope

get_size_of = arch.get_size_of

__all__ = [
    "Tensor",
    "Chip",
    "ProfDataRegister",
    "PrefModel",
    "get_size_of",
    "ComputationInstruction",
    "InstrApiRegister",
    "Core",
    "set_flag",
    "wait_flag",
    "VecScope"
]
