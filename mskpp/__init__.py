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

from .apis import mmad, vadd, vadds, vmul, vmuls, vexp, vsub, vln, vmax, vector_dup, vbrcb, vconv, vdiv, vcadd, \
    vtranspose, vcgmax, vmaxs, vcmax, vabs, vaddreluconv, vaddrelu, vand, vaxpy, vsel, vshl, vshr, vsqrt, \
    vsubreluconv, vsubrelu, vcgadd, vcgmin, vcmin, vcmp, vcmpv, vcmpvs, vcopy, vcpadd, vmin, vmins, vrelu, vnot, \
    vmaddrelu, vmla, vreducev2, vreduce, vrsqrt, vor, vmulconv, vmaddrelu, vmla, vreducev2, vreduce, vgather, \
    vgatherb, vrec, vlrelu, vmadd, vbitsort, vmrgsort, vconv_deq, vconv_vdeq, rv_vadd, rv_vsub, rv_vmax, rv_vmin, \
    rv_vabsdif, rv_vadds

from .core import Tensor, Chip, Core, set_flag, wait_flag, VecScope

try:
    from mskl import *
except Exception as e:
    print("warning: package mskl not found")

__all__ = [
    "Tensor",
    "Chip",
    "Core",
    "set_flag",
    "wait_flag",
    "VecScope",
    "mmad",
    "vadd",
    "rv_vadd",
    "rv_vsub",
    "rv_vmax",
    "rv_vmin",
    "rv_vabsdif",
    "rv_vadds",
    "vadds",
    "vmul",
    "vmuls",
    "vexp",
    "vsub",
    "vln",
    "vmax",
    "vector_dup",
    "vbrcb",
    "vconv",
    "vdiv",
    "vcadd",
    "vtranspose",
    "vcgmax",
    "vmaxs",
    "vrec",
    "vrsqrt",
    "vsel",
    "vshl",
    "vshr",
    "vsqrt",
    "vsubreluconv",
    "vsubrelu",
    "vcmax",
    "vabs",
    "vaddreluconv",
    "vaddrelu",
    "vand",
    "vaxpy",
    "vcgadd",
    "vcgmin",
    "vcmin",
    "vcmp",
    "vcmpv",
    "vcmpvs",
    "vcopy",
    "vcpadd",
    "vmin",
    "vmins",
    "vrelu",
    "vnot",
    "vmaddrelu",
    "vmla",
    "vreducev2",
    "vreduce",
    "vor",
    "vmulconv",
    "vreduce",
    "vgather",
    "vgatherb",
    "vlrelu",
    "vmadd",
    "vbitsort",
    "vmrgsort",
    "vconv_deq",
    "vconv_vdeq",
]
