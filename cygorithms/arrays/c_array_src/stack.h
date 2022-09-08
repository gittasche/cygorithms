#ifndef CYGORITHMS_STACK_H
#define CYGORITHMS_STACK_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <stddef.h>
#include <stdbool.h>
#include "dynonedarray.h"
#include "../c_util/util.h"

typedef struct {
    PyObject_HEAD
    DynamicOneDArray* _data;
} ArrayStack;

static void ArrayStack_dealloc(DynamicOneDArray *self)
{
    DynamicOneDArray_dealloc(self->_one_d_array);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* ArrayStack___new__(PyTypeObject* type, PyObject *args, PyObject *kwds)
{
    ArrayStack *self;
    self = (ArrayStack*)type->tp_alloc(type, 0);
    PyObject *_one_d_array = DynamicOneDArray___new__(&DynamicOneDArrayType, args, kwds);
    if (!_one_d_array)
        return NULL;

    self->_data = _one_d_array;

    return (PyObject*)self;
}

static PyObject* ArrayStack_is_empty(ArrayStack *self)
{
    bool is_empty = self->_data->_last_pos_filled == -1;

    if (is_empty)
        Py_RETURN_TRUE;
    
    Py_RETURN_FALSE;
}

static Py_ssize_t ArrayStack___len__(ArrayStack *self)
{
    return DynamicOneDArray___len__(self->_data);
}

static PyObject* ArrayStack_push(ArrayStack *self, PyObject *args)
{
    size_t len_args = PyObject_Length(args);
    if (len_args != 1)
    {
        PyErr_SetString(
            PyExc_ValueError,
            "Expected one argument to push."
        );
    }

    if (PyObject_IsTrue(ArrayStack_is_empty(self)))
    {
        self->_data->_one_d_array->_dtype = (PyObject*)Py_TYPE(PyObject_GetItem(args, PyLong_FromLong(0)));
    }
    else
    {
        set_exception_if_dtype_mismatch(self->_data->_one_d_array->_dtype, PyObject_GetItem(args, PyLong_FromLong(0)));
    }

    DynamicOneDArray_append(self->_data, args);

    Py_RETURN_NONE;
}

static PyObject *ArrayStack_pop(ArrayStack *self)
{
    if (PyObject_IsTrue(ArrayStack_is_empty(self)))
    {
        PyErr_SetString(PyExc_IndexError, "ArrayStack is empty.");
        return NULL;
    }

    PyObject *top_element = DynamicOneDArray___getitem__(self->_data, PyLong_FromLong(self->_data->_last_pos_filled));
    PyObject *last_pos_arg = PyTuple_Pack(1, PyLong_FromLong(self->_data->_last_pos_filled));
    DynamicOneDArray_delete(self->_data, last_pos_arg);
    return top_element;
}

static PyObject *ArrayStack_peek(ArrayStack *self, void *closure)
{
    return DynamicOneDArray___getitem__(self->_data, PyLong_FromSize_t(self->_data->_last_pos_filled));
}

static struct PyMethodDef ArrayStack_PyMethodDef[] = {
    {"is_empty", (PyCFunction)ArrayStack_is_empty, METH_VARARGS, NULL},
    {"push", (PyCFunction)ArrayStack_push, METH_VARARGS, NULL},
    {"pop", (PyCFunction)ArrayStack_pop, METH_VARARGS, NULL},
    {"peek", (PyCFunction)ArrayStack_peek, METH_VARARGS, NULL},
    {NULL}
};

static PyMappingMethods ArrayStack_PyMappingMethods = {
    (lenfunc)ArrayStack___len__,
};

static PyTypeObject ArrayStackType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "ArrayStack",
    /* tp_basicsize */ sizeof(ArrayStack),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)ArrayStack_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ &ArrayStack_PyMappingMethods,
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
    /* tp_methods */ ArrayStack_PyMethodDef,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ 0,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ ArrayStack___new__,
};

#endif // CYGORITHMS_STACK_H