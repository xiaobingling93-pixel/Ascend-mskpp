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
from abc import ABC, abstractmethod
from .common.registries import BaseRegistry


class PrefModel(ABC):
    """
    通过性能数据建模，获得指令在特定输入输出下的性能数据
    """
    def __init__(self, name, inputs, outputs):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    @abstractmethod
    def size(self):
        raise Exception("this api need to impl.")

    @abstractmethod
    def time(self):
        raise Exception("this api need to impl.")

    @abstractmethod
    def pipe_name(self):
        raise Exception("this api need to impl.")


class ProfDataRegister(BaseRegistry):
    """性能数据注册器，继承自基础注册器"""
    @classmethod
    def is_prof_data_exist(cls, name):  # if mov path in register then do not use self mov path
        return cls.get(name) is not None


def import_all_pref_datas():
    import importlib
    module_names = []
    api_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prof_data")
    for fname in os.listdir(api_dir):
        if os.path.isfile(os.path.join(api_dir, fname)) \
                and fname.endswith('prof.py') and not fname.startswith("ascend"):
            module_names.append(fname.split('.')[0])
    for module_name in module_names:
        importlib.import_module(f'.prof_data.{module_name}', package='mskpp')


import_all_pref_datas()