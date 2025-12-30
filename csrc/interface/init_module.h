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

#ifndef WORKLOAD_ANALYSIS_MSKPP_INIT_MODULE_H
#define WORKLOAD_ANALYSIS_MSKPP_INIT_MODULE_H

#include <Python.h>
namespace Mskpp {
// init arch module
PyObject *InitArchInfoModule();

// init prof data module
PyObject *InitProfdataModule();

// init task schedule module
PyObject *InitTaskScheduleModule();

PyObject* BasePyNew(PyTypeObject *type, PyObject *args, PyObject *kwds);

/* c++ don't support non-trivial designated initializers, so define a marco */
#define MSKPP_DEFINE_CLASS_NOMEMBER(varname, name, methods, doc) static PyTypeObject varname = { \
    PyVarObject_HEAD_INIT(nullptr, 0) \
    (name),                               /* tp_name */ \
    0,                                  /* tp_basicsize */ \
    0,                                  /* tp_itemsize */ \
    0,                                  /* tp_dealloc */ \
    0,                                  /* tp_vectorcall_offset */ \
    0,                                  /* tp_getattr */ \
    0,                                  /* tp_setattr */ \
    0,                                  /* tp_as_async */ \
    0,                                  /* tp_repr */ \
    0,                                  /* tp_as_number */ \
    0,                                  /* tp_as_sequence */ \
    0,                                  /* tp_as_mapping */ \
    0,                                  /* tp_hash */ \
    0,                                  /* tp_call */ \
    0,                                  /* tp_str */ \
    0,                                  /* tp_getattro */ \
    0,                                  /* tp_setattro */ \
    0,                                  /* tp_as_buffer */ \
    (Py_TPFLAGS_DEFAULT),                 /* tp_flags */ \
    (doc),                                /* tp_doc */ \
    0,                                  /* tp_traverse */ \
    0,                                  /* tp_clear */ \
    0,                                  /* tp_richcompare */ \
    0,                                  /* tp_weaklistoffset */ \
    0,                                  /* tp_iter */ \
    0,                                  /* tp_iternext */ \
    (methods),                            /* tp_methods */ \
    0,                                  /* tp_members */ \
    0,                                  /* tp_getset */ \
    (&PyBaseObject_Type),                 /* tp_base */ \
    0,                                  /* tp_dict */ \
    0,                                  /* tp_descr_get */ \
    0,                                  /* tp_descr_set */ \
    0,                                  /* tp_dictoffset */ \
    0,                                  /* tp_init */ \
    0,                                  /* tp_alloc */ \
    BasePyNew,                          /* tp_new */ \
    0,                                  /* tp_free */ \
}
}
#endif // WORKLOAD_ANALYSIS_MSKPP_INIT_MODULE_H
