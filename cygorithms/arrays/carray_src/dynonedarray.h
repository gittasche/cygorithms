#ifndef CYGORITHMS_DYNONEDARRAY_H
#define CYGORITHMS_DYNONEDARRAY_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <stddef.h>
#include <stdlib.h>
#include "dynarray.h"
#include "onedarray.h"
#include "util.h"

typedef struct {
    PyObject_HEAD
    OneDArray *_one_d_array;
    double _load_factor;
    size_t _num;
    size_t _last_pos_filled;
    size_t _size;
} DynamicOneDArray;

static void DynamicOneDArray_dealloc(DynamicOneDArray *self)
{
    OneDArray_dealloc(self->_one_d_array);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* DynamicOneDArray___new__(PyTypeObject* type, PyObject *args, PyObject *kwds)
{
    DynamicOneDArray *self;
    self = (DynamicOneDArray*)type->tp_alloc(type, 0);
    PyObject *_one_d_array = OneDArray___new__(&OneDArrayType, args, kwds);
    if (!_one_d_array)
        return NULL;

    self->_one_d_array = (OneDArray*)_one_d_array;
    self->_size = self->_one_d_array->_size;

    PyObject *_load_factor = PyObject_GetItem(kwds, PyUnicode_FromString("load_factor"));
    if (_load_factor == NULL)
    {
        PyErr_Clear();
        self->_load_factor = 0.25;
    }
    else
    {
        _load_factor = PyFloat_FromString(PyObject_Str(_load_factor));
        if (!_load_factor)
            return NULL;
        self->_load_factor = PyFloat_AS_DOUBLE(_load_factor);
    }
    if (self->_one_d_array->_size == 0 || self->_one_d_array->_data[0] == Py_None)
        self->_num = 0;
    else
        self->_num = self->_one_d_array->_size;
    self->_last_pos_filled = self->_num - 1;

    return (PyObject*)self;
}

static PyObject* DynamicOneDArray___getitem__(DynamicOneDArray *self, PyObject *arg)
{
    return OneDArray___getitem__(self->_one_d_array, arg);
}

static int DynamicOneDArray___setitem__(DynamicOneDArray *self, PyObject *arg, PyObject *value)
{
    return OneDArray___setitem__(self->_one_d_array, arg, value);
}

static Py_ssize_t DynamicOneDArray___len__(DynamicOneDArray *self)
{
    return OneDArray___len__(self->_one_d_array);
}

static PyMappingMethods DynamicOneDArray_PyMappingMethods = {
    (lenfunc)DynamicOneDArray___len__,
    (binaryfunc)DynamicOneDArray___getitem__,
    (objobjargproc)DynamicOneDArray___setitem__,
};

static PyObject* DynamicOneDArray_fill(DynamicOneDArray *self, PyObject *args)
{
    return OneDArray_fill(self->_one_d_array, args);
}

static PyObject* DynamicOneDArray__modify(DynamicOneDArray *self, PyObject *args)
{
    PyObject *force = NULL;
    if (args)
        force = PyObject_GetItem(args, PyLong_FromLong(0));
    if (!force)
    {
        PyErr_Clear();
        force = Py_False;
    }

    long i, j;
    PyObject **_data = self->_one_d_array->_data;
    size_t _size = self->_one_d_array->_size;
    if (force == Py_True)
    {
        i = -1;
        j = _size - 1;
        while (_data[j] == Py_None)
        {
            i--;
            j--;
        }
        self->_last_pos_filled = i + _size;
    }

    if ((float)self->_num / self->_size < self->_load_factor)
    {
        long new_size = 2 * self->_num + 1;
        PyObject **arr_new = (PyObject**)malloc(new_size * sizeof(PyObject*));
        for (i = 0; i < new_size; ++i)
        {
            Py_INCREF(Py_None);
            arr_new[i] = Py_None;
        }
        long j = 0;
        for (i = 0; i <= self->_last_pos_filled; ++i)
        {
            if (_data[i] != Py_None)
            {
                Py_INCREF(Py_None);
                arr_new[j] = _data[i];
                j += 1;
            }
        }
        self->_last_pos_filled = j - 1;
        self->_one_d_array->_data = arr_new;
        self->_one_d_array->_size = new_size;
        self->_size = new_size;
    }

    Py_RETURN_NONE;
}

static PyObject* DynamicOneDArray_append(DynamicOneDArray *self, PyObject *args)
{
    PyObject *el = PyObject_GetItem(args, PyLong_FromLong(0));
    if (!el)
        return NULL;

    size_t _size = self->_one_d_array->_size;
    PyObject **_data = self->_one_d_array->_data;
    if (self->_last_pos_filled + 1 == _size)
    {
        long new_size = 2 * _size + 1;
        PyObject **arr_new = (PyObject**)malloc(new_size * sizeof(PyObject*));

        long i;
        for (i = 0; i <= self->_last_pos_filled; ++i)
            arr_new[i] = _data[i];

        for ( ; i < new_size; ++i)
        {
            arr_new[i] = Py_None;
        }
        arr_new[self->_last_pos_filled + 1] = el;
        self->_one_d_array->_size = new_size;
        self->_size = new_size;
        self->_one_d_array->_data = arr_new;
    }
    else
    {
        _data[self->_last_pos_filled + 1] = el;
    }
    self->_last_pos_filled += 1;
    self->_num += 1;
    return DynamicOneDArray__modify(self, NULL);
}

static PyObject* DynamicOneDArray_delete(DynamicOneDArray *self, PyObject *args)
{
    PyObject *idx_pyobject = PyObject_GetItem(args, PyLong_FromLong(0));
    if (!idx_pyobject)
        return NULL;

    long idx = PyLong_AsLong(idx_pyobject);
    if (idx == -1 && PyErr_Occurred())
        return NULL;
    
    PyObject **_data = self->_one_d_array->_data;
    if (idx <= self->_last_pos_filled && idx >= 0 && _data[idx] != Py_None)
    {
        _data[idx] = Py_None;
        self->_num -= 1;
        if (self->_last_pos_filled == idx)
            self->_last_pos_filled -= 1;
    return DynamicOneDArray__modify(self, NULL);
    }

    Py_RETURN_NONE;
}

static struct PyMethodDef DynamicOneDArray_PyMethodDef[] = {
    {"fill", (PyCFunction)DynamicOneDArray_fill, METH_VARARGS, NULL},
    {"_modify", (PyCFunction)DynamicOneDArray__modify, METH_VARARGS, NULL},
    {"append", (PyCFunction)DynamicOneDArray_append, METH_VARARGS, NULL},
    {"delete", (PyCFunction)DynamicOneDArray_delete, METH_VARARGS, NULL},
    {NULL}
};

static struct PyMemberDef DynamicOneDArray_PyMemberDef[] = {
    {"size", T_PYSSIZET, offsetof(DynamicOneDArray, _size), READONLY, NULL},
    {"_num", T_PYSSIZET, offsetof(DynamicOneDArray, _num), READONLY, NULL},
    {"_last_pos_filled", T_PYSSIZET, offsetof(DynamicOneDArray, _last_pos_filled), READONLY, NULL},
    {NULL}
};

static PyTypeObject DynamicOneDArrayType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "DynamicOneDArray",
    /* tp_basicsize */ sizeof(DynamicOneDArray),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)DynamicOneDArray_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ &DynamicOneDArray_PyMappingMethods,
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
    /* tp_methods */ DynamicOneDArray_PyMethodDef,
    /* tp_members */ DynamicOneDArray_PyMemberDef,
    /* tp_getset */ 0,
    /* tp_base */ &DynamicArrayType,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ DynamicOneDArray___new__,
};

#endif // CYGORITHMS_DYNONEDARRAY_H