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

class BaseRegistry:
    """基础注册器类"""
    _registry = {}

    @classmethod
    def register(cls, name):
        """
        注册器装饰器，用于将类注册到当前注册器中
        :param name: 注册的名称
        :return: 装饰器函数
        """
        def decorator(sub_cls):
            key = f"{cls.__name__}:{name}"  # 生成唯一的键，格式为 子类名:注册名称
            cls._registry[key] = sub_cls    # 将类注册到注册表中
            return sub_cls
        return decorator

    @classmethod
    def get(cls, name):
        """
        根据名称从当前注册器中获取已注册的类
        :param name: 注册的名称
        :return: 已注册的类，如果未找到则返回 None
        """
        key = f"{cls.__name__}:{name}"      # 生成查找的键
        return cls._registry.get(key, None)
