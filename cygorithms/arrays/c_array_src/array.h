#ifndef CYGORITHMS_ARRAY_H
#define CYGORITHMS_ARRAY_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

typedef struct {
    PyObject_HEAD
} Array;

static void Array_dealloc(Array *self)
{
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* Array___new__(PyTypeObject* type, PyObject* args, PyObject* kwds)
{
    Array *self;
    self = (Array*)type->tp_alloc(type, 0);
    return (PyObject*)self;
}

static PyTypeObject ArrayType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "Array",
    /* tp_basicsize */ sizeof(Array),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)Array_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ 0,
    /* tp_hash  */ 0,
    /* tp_call */ 0,
    /* tp_str */ 0,
    /* tp_getattro */ 0,
    /* tp_setattro */ 0,
    /* tp_as_buffer */ 0,
    /* tp_flags */ Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    /* tp_doc */ 0,
    /* tp_traverse */ 0,
    /* tp_clear */ 0,
    /* tp_richcompare */ 0,
    /* tp_weaklistoffset */ 0,
    /* tp_iter */ 0,
    /* tp_iternext */ 0,
    /* tp_methods */ 0,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ 0,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ Array___new__,
};

#endif // CYGORITHMS_ARRAY_H