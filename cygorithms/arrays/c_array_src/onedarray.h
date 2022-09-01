#ifndef CYGORITHMS_ONEDARRAY_H
#define CYGORITHMS_ONEDARRAY_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <stddef.h>
#include <stdlib.h>
#include <stdio.h>
#include "array.h"
#include "../c_util/util.h"

typedef struct
{
    PyObject_HEAD
    size_t _size;
    PyObject** _data;
    PyObject* _dtype;
} OneDArray;

static void OneDArray_dealloc(OneDArray *self)
{
    free(self->_data);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject *OneDArray___new__(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    OneDArray *self;
    self = (OneDArray*)type->tp_alloc(type, 0);
    size_t len_args = PyObject_Length(args);

    // Check dtype only for first element
    PyObject *dtype = PyObject_GetItem(args, PyLong_FromLong(0));
    // case not dtype provided
    if (dtype == Py_None)
    {
        PyErr_SetString(PyExc_ValueError, "Data type is not defined.");
        return NULL;
    }
    self->_dtype = dtype;

    // cases with dtype provided
    /// case only dtype provided
    if (len_args != 2 && len_args != 3)
    {
        PyErr_SetString(
            PyExc_ValueError,
            "Too few arguments to create Array,"
            " pass either size of the Array,"
            " or list of elements both."
        );
        return NULL;
    }

    /// case both data and size provided
    if (len_args == 3)
    {
        PyObject *args0 = PyObject_GetItem(args, PyLong_FromLong(1));
        PyObject *args1 = PyObject_GetItem(args, PyLong_FromLong(2));
        size_t size;
        PyObject *data = NULL;
        if ((PyList_Check(args0) || PyTuple_Check(args0)) && PyLong_Check(args1))
        {
            size = PyLong_AsUnsignedLong(args1);
            data = args0;
        }
        else if (PyLong_Check(args0) && (PyList_Check(args1) || PyTuple_Check(args1)))
        {
            size = PyLong_AsUnsignedLong(args0);
            data = args1;
        }
        else
        {
            PyErr_Format(
                PyExc_TypeError,
                "expected `size` of integer type, got %s and"
                " `data` as list or tuple instance, got %s.",
                PyObject_AsString(PyObject_Repr(PyObject_Type(args0))),
                PyObject_AsString(PyObject_Repr(PyObject_Type(args1)))
            );
            return NULL;
        }
        size_t len_data = PyObject_Length(data);
        if (size != len_data)
        {
            PyErr_Format(
                PyExc_ValueError,
                "length of `data` must be equal `size`,"
                " got %d and %d",
                size, len_data
            );
            return NULL;
        }
        self->_size = size;
        self->_data = (PyObject**)malloc(size * sizeof(PyObject*));
        for (size_t i = 0; i < size; ++i)
        {
            PyObject *value = PyObject_GetItem(data, PyLong_FromSize_t(i));
            if (raise_exception_if_dtype_mismatch(value, self->_dtype))
                return NULL;
            self->_data[i] = value;
        }
    }
    else if (len_args == 2)
    {
        PyObject *args0 = PyObject_GetItem(args, PyLong_FromLong(1));
        if (PyLong_Check(args0))
        {
            self->_size = PyLong_AsSize_t(args0);
            PyObject *data = PyObject_GetItem(kwds, PyUnicode_FromString("data"));
            if (data == NULL)
            {
                PyErr_Clear();
                data = Py_None;
            }
            else if (raise_exception_if_dtype_mismatch(data, self->_dtype))
                return NULL;
            self->_data = (PyObject**)malloc(self->_size * sizeof(PyObject*));
            for (size_t i = 0; i < self->_size; ++i)
                self->_data[i] = data;
        }
        else if (PyList_Check(args0) || PyTuple_Check(args0))
        {
            self->_size = PyObject_Length(args0);
            self->_data = (PyObject**)malloc(self->_size * sizeof(PyObject*));
            for (size_t i = 0; i < self->_size; ++i)
            {
                PyObject *value = PyObject_GetItem(args0, PyLong_FromSize_t(i));
                if (raise_exception_if_dtype_mismatch(value, self->_dtype))
                    return NULL;
                self->_data[i] = value;
            }
        }
        else
        {
            PyErr_Format(
                PyExc_TypeError,
                "expected `size` of integer type, got %s or"
                " `data` as list or tuple instance, got %s.",
                PyObject_AsString(PyObject_Repr(PyObject_Type(args0))),
                PyObject_AsString(PyObject_Repr(PyObject_Type(args0)))
            );
            return NULL;
        }
    }

    return (PyObject*)self;
}

static int OneDArray___setitem__(OneDArray *self, PyObject *arg, PyObject *value)
{
    size_t idx = PyLong_AsUnsignedLong(arg);
    if (value == Py_None)
    {
        self->_data[idx] = value;
    }
    else if (!set_exception_if_dtype_mismatch(value, self->_dtype))
    {
        self->_data[idx] = value;
    }
    return 0;
}

static PyObject* OneDArray___getitem__(OneDArray *self, PyObject *arg)
{
    size_t idx = PyLong_AsUnsignedLong(arg);
    if (idx >= self->_size)
    {
        PyErr_Format(
            PyExc_IndexError,
            "Index, %d, out of range, [%d, %d)",
            idx, 0, self->_size
        );
        return NULL;
    }
    Py_INCREF(self->_data[idx]);
    return self->_data[idx];
}

static Py_ssize_t OneDArray___len__(OneDArray *self)
{
    return self->_size;
}

static PyMappingMethods OneDArray_PyMappingMethods = {
    (lenfunc)OneDArray___len__,
    (binaryfunc)OneDArray___getitem__,
    (objobjargproc)OneDArray___setitem__,
};

static PyObject* OneDArray_fill(OneDArray *self, PyObject *args)
{
    PyObject *value = PyObject_GetItem(args, PyLong_FromLong(0));
    if (raise_exception_if_dtype_mismatch(value, self->_dtype))
    {
        return NULL;
    }
    for (size_t i = 0; i < self->_size; ++i)
    {
        self->_data[i] = value;
    }
    Py_RETURN_NONE;
}

static struct PyMethodDef OneDArray_PyMethodDef[] = {
    {"fill", (PyCFunction)OneDArray_fill, METH_VARARGS, NULL},
    {NULL}
};

static struct PyMemberDef OneDArray_PyMemberDef[] = {
    {"size", T_PYSSIZET, offsetof(OneDArray, _size), READONLY, NULL},
    {NULL}
};

static PyTypeObject OneDArrayType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "OneDArray",
    /* tp_basicsize */ sizeof(OneDArray),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)OneDArray_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ &OneDArray_PyMappingMethods,
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
    /* tp_methods */ OneDArray_PyMethodDef,
    /* tp_members */ OneDArray_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &ArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ OneDArray___new__,
};

#endif // CYGORITHMS_ONEDARRAY_H