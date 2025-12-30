/* -------------------------------------------------------------------------
 * This file is part of the MindStudio project.
 * Copyright (c) 2025 Huawei Technologies Co.,Ltd.
 *
 * MindStudio is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *
 *          http://license.coscl.org.cn/MulanPSL2
 *
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 * ------------------------------------------------------------------------- */

#include "data_model_define.h"
namespace Mskpp {

// 定义各个指令的类
INSTR_CLASS_DEFINE_NO_PARA(Mmad, Mmad);
INSTR_CLASS_DEFINE_NO_PARA(Mov, Mov);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vabs, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vadd, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vaddrelu, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vaddreluconv, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vadds, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vand, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vaxpy, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vbrcb, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcadd, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcgadd, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcgmax, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcgmin, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcmax, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcmin, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcmp, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcmpv, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcmpvs, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcopy, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vconv, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vconvdeq, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vconvvdeq, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vcpadd, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vdiv, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(VectorDup, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vexp, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vln, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vlrelu, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmadd, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmax, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmaxs, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmin, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmins, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmrgsort, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmul, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmuls, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vnot, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vor, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vrelu, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vrec, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vsub, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vrsqrt, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vsel, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vshl, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vshr, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vsqrt, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(VsubReluConv, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(VsubRelu, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(VmaddRelu, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmla, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vreducev2, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vreduce, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vgather, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vgatherb, Vec);
INSTR_CLASS_DEFINE_SINGLE_PARA(Vmulconv, Vec);

// 注册各个指令类
DataRegister<MmadClass, MmadData> mmad("MMAD");
DataRegister<MovClass, MovData> mov("MOV");
DataRegister<VecClass, VabsData, std::string> Vabs_("VABS");
DataRegister<VecClass, VaddData, std::string> Vadd_("VADD");
DataRegister<VecClass, VaddreluData, std::string> Vaddrelu_("VADDRELU");
DataRegister<VecClass, VaddreluconvData, std::string> Vaddreluconv_("VADDRELUCONV");
DataRegister<VecClass, VaddsData, std::string> Vadds_("VADDS");
DataRegister<VecClass, VandData, std::string> Vand_("VAND");
DataRegister<VecClass, VaxpyData, std::string> Vaxpy_("VAXPY");
DataRegister<VecClass, VbrcbData, std::string> Vbrcb_("VBRCB");
DataRegister<VecClass, VcaddData, std::string> Vcadd_("VCADD");
DataRegister<VecClass, VcgaddData, std::string> Vcgadd_("VCGADD");
DataRegister<VecClass, VcgmaxData, std::string> Vcgmax_("VCGMAX");
DataRegister<VecClass, VcgminData, std::string> Vcgmin_("VCGMIN");
DataRegister<VecClass, VcmaxData, std::string> Vcmax_("VCMAX");
DataRegister<VecClass, VcminData, std::string> Vcmin_("VCMIN");
DataRegister<VecClass, VcmpData, std::string> Vcmp_("VCMP");
DataRegister<VecClass, VcmpvData, std::string> Vcmpv_("VCMPV");
DataRegister<VecClass, VcmpvsData, std::string> Vcmpvs_("VCMPVS");
DataRegister<VecClass, VcopyData, std::string> Vcopy_("VCOPY");
DataRegister<VecClass, VconvData, std::string> Vconv_("VCONV");
DataRegister<VecClass, VconvdeqData, std::string> Vconvdeq_("VCONVDEQ");
DataRegister<VecClass, VconvvdeqData, std::string> Vconvvdeq_("VCONVVDEQ");
DataRegister<VecClass, VcpaddData, std::string> Vcpadd_("VCPADD");
DataRegister<VecClass, VdivData, std::string> Vdiv_("VDIV");
DataRegister<VecClass, VectorDupData, std::string> VectorDup_("VECTORDUP");
DataRegister<VecClass, VexpData, std::string> Vexp_("VEXP");
DataRegister<VecClass, VlnData, std::string> Vln_("VLN");
DataRegister<VecClass, VlreluData, std::string> Vlrelu_("VLRELU");
DataRegister<VecClass, VmaddData, std::string> Vmadd_("VMADD");
DataRegister<VecClass, VmaxData, std::string> Vmax_("VMAX");
DataRegister<VecClass, VmaxsData, std::string> Vmaxs_("VMAXS");
DataRegister<VecClass, VminData, std::string> Vmin_("VMIN");
DataRegister<VecClass, VminsData, std::string> Vmins_("VMINS");
DataRegister<VecClass, VmrgsortData, std::string> Vmrgsort_("VMRGSORT");
DataRegister<VecClass, VmulData, std::string> Vmul_("VMUL");
DataRegister<VecClass, VmulsData, std::string> Vmuls_("VMULS");
DataRegister<VecClass, VnotData, std::string> Vnot_("VNOT");
DataRegister<VecClass, VorData, std::string> Vor_("VOR");
DataRegister<VecClass, VreluData, std::string> Vrelu_("VRELU");
DataRegister<VecClass, VrecData, std::string> Vrec_("VREC");
DataRegister<VecClass, VsubData, std::string> Vsub_("VSUB");
DataRegister<VecClass, VrsqrtData, std::string> Vrsqrt_("VRSQRT");
DataRegister<VecClass, VselData, std::string> Vsel_("VSEL");
DataRegister<VecClass, VshlData, std::string> Vshl_("VSHL");
DataRegister<VecClass, VshrData, std::string> Vshr_("VSHR");
DataRegister<VecClass, VsqrtData, std::string> Vsqrt_("VSQRT");
DataRegister<VecClass, VsubReluConvData, std::string> VsubReluConv_("VSUBRELUCONV");
DataRegister<VecClass, VsubReluData, std::string> VsubRelu_("VSUBRELU");
DataRegister<VecClass, VmaddReluData, std::string> VmaddRelu_("VMADDRELU");
DataRegister<VecClass, VmlaData, std::string> Vmla_("VMLA");
DataRegister<VecClass, Vreducev2Data, std::string> Vreducev2_("VREDUCEV2");
DataRegister<VecClass, VreduceData, std::string> Vreduce_("VREDUCE");
DataRegister<VecClass, VmulconvData, std::string> Vmulconv_("VMULCONV");
DataRegister<VecClass, Vreducev2Data, std::string> Vgather("VGATHER");
DataRegister<VecClass, VreduceData, std::string> Vgatherb("VGATHERB");
}