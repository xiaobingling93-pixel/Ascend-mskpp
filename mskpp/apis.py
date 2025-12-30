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

from .core import InstrApiRegister

mmad = InstrApiRegister.get("MMAD")
vadd = InstrApiRegister.get("VADD")
rv_vadd = InstrApiRegister.get("RV_VADD")
rv_vsub = InstrApiRegister.get("RV_VSUB")
rv_vmax = InstrApiRegister.get("RV_VMAX")
rv_vmin = InstrApiRegister.get("RV_VMIN")
rv_vabsdif = InstrApiRegister.get("RV_VABSDIF")
rv_vadds = InstrApiRegister.get("RV_VADDS")
vadds = InstrApiRegister.get("VADDS")
vmul = InstrApiRegister.get("VMUL")
vmuls = InstrApiRegister.get("VMULS")
vexp = InstrApiRegister.get("VEXP")
vsub = InstrApiRegister.get("VSUB")
vln = InstrApiRegister.get("VLN")
vmax = InstrApiRegister.get("VMAX")
vconv = InstrApiRegister.get("VCONV")
vbrcb = InstrApiRegister.get("VBRCB")
vector_dup = InstrApiRegister.get("VECTORDUP")
vcadd = InstrApiRegister.get("VCADD")
vdiv = InstrApiRegister.get("VDIV")
vtranspose = InstrApiRegister.get("VTRANSPOSE")
vcgmax = InstrApiRegister.get("VCGMAX")
vmaxs = InstrApiRegister.get("VMAXS")
vcmax = InstrApiRegister.get("VCMAX")
vabs = InstrApiRegister.get("VABS")
vaddreluconv = InstrApiRegister.get("VADDRELUCONV")
vaddrelu = InstrApiRegister.get("VADDRELU")
vand = InstrApiRegister.get("VAND")
vaxpy = InstrApiRegister.get("VAXPY")
vrsqrt = InstrApiRegister.get("VRSQRT")
vsel = InstrApiRegister.get("VSEL")
vshl = InstrApiRegister.get("VSHL")
vshr = InstrApiRegister.get("VSHR")
vsqrt = InstrApiRegister.get("VSQRT")
vsubreluconv = InstrApiRegister.get("VSUBRELUCONV")
vsubrelu = InstrApiRegister.get("VSUBRELU")
vcgadd = InstrApiRegister.get("VCGADD")
vcgmin = InstrApiRegister.get("VCGMIN")
vcmin = InstrApiRegister.get("VCMIN")
vcmp = InstrApiRegister.get("VCMP")
vcmpv = InstrApiRegister.get("VCMPV")
vcmpvs = InstrApiRegister.get("VCMPVS")
vcopy = InstrApiRegister.get("VCOPY")
vcpadd = InstrApiRegister.get("VCPADD")
vmin = InstrApiRegister.get("VMIN")
vmins = InstrApiRegister.get("VMINS")
vrelu = InstrApiRegister.get("VRELU")
vnot = InstrApiRegister.get("VNOT")
vrec = InstrApiRegister.get("VREC")
vmaddrelu = InstrApiRegister.get("VMADDRELU")
vmla = InstrApiRegister.get("VMLA")
vreducev2 = InstrApiRegister.get("VREDUCEV2")
vreduce = InstrApiRegister.get("VREDUCE")
vor = InstrApiRegister.get("VOR")
vmulconv = InstrApiRegister.get("VMULCONV")
vgather = InstrApiRegister.get("VGATHER")
vgatherb = InstrApiRegister.get("VGATHERB")
vlrelu = InstrApiRegister.get("VLRELU")
vmadd = InstrApiRegister.get("VMADD")
vbitsort = InstrApiRegister.get("VBITSORT")
vmrgsort = InstrApiRegister.get("VMRGSORT")
vconv_deq = InstrApiRegister.get("VCONVDEQ")
vconv_vdeq = InstrApiRegister.get("VCONVVDEQ")