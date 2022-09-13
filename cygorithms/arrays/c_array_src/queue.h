#ifndef CYGORITHMS_QUEUE_H
#define CYGORITHMS_QUEUE_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <stddef.h>
#include <stdbool.h>
#include "dynonedarray.h"
#include "../c_util/util.h"

typedef struct {
    PyObject_HEAD
    size_t _first_pos_filled;
    DynamicOneDArray *_data;
} ArrayQueue;

static void ArrayQueue_dealloc(ArrayQueue *self)
{
    DynamicOneDArray_dealloc(self->_data);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* ArrayQueue___new__(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    ArrayQueue *self;
    self = (ArrayQueue*)type->tp_alloc(type, 0);
    PyObject *_one_d_array = DynamicOneDArray___new__(&DynamicOneDArrayType, args, kwds);
    if (!_one_d_array)
        return NULL;

    self->_data = (DynamicOneDArray*)_one_d_array;
    self->_first_pos_filled = 0;
    return (PyObject*)self;
}

static PyObject* ArrayQueue_is_empty(ArrayQueue *self)
{
    bool is_empty = self->_data->_last_pos_filled == -1;

    if (is_empty)
        Py_RETURN_TRUE;
    
    Py_RETURN_FALSE;
}

static Py_ssize_t ArrayQueue___len__(ArrayQueue *self)
{
    return DynamicOneDArray___len__(self->_data);
}

static PyObject* ArrayQueue_push(ArrayQueue *self, PyObject *args)
{
    size_t len_args = PyObject_Length(args);
    if (len_args != 1)
    {
        PyErr_SetString(
            PyExc_ValueError,
            "Expected one argument to push."
        );
    }

    if (PyObject_IsTrue(ArrayQueue_is_empty(self)))
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

static PyObject *ArrayQueue_pop(ArrayQueue *self)
{
    if (PyObject_IsTrue(ArrayQueue_is_empty(self)))
    {
        PyErr_SetString(PyExc_IndexError, "ArrayQueue is empty.");
        return NULL;
    }

    size_t old_size = self->_data->_size;
    PyObject *first_element = DynamicOneDArray___getitem__(self->_data, PyLong_FromLong(self->_first_pos_filled));
    PyObject *last_pos_arg = PyTuple_Pack(1, PyLong_FromLong(self->_first_pos_filled));
    DynamicOneDArray_delete(self->_data, last_pos_arg);
    if (self->_data->_size != old_size)
        self->_first_pos_filled = 0;
    else
        self->_first_pos_filled++;
    return first_element;
}

static PyObject *ArrayQueue_peek(ArrayQueue *self, void *closure)
{
    return DynamicOneDArray___getitem__(self->_data, PyLong_FromSize_t(self->_first_pos_filled));
}

static struct PyMethodDef ArrayQueue_PyMethodDef[] = {
    {"is_empty", (PyCFunction)ArrayQueue_is_empty, METH_VARARGS, NULL},
    {"push", (PyCFunction)ArrayQueue_push, METH_VARARGS, NULL},
    {"pop", (PyCFunction)ArrayQueue_pop, METH_VARARGS, NULL},
    {"peek", (PyCFunction)ArrayQueue_peek, METH_VARARGS, NULL},
    {NULL}
};

static PyMappingMethods ArrayQueue_PyMappingMethods = {
    (lenfunc)ArrayQueue___len__,
};

static PyTypeObject ArrayQueueType = {
    /* tp_name */ PyVarObject_HEAD_INIT(NULL, 0) "ArrayQueue",
    /* tp_basicsize */ sizeof(ArrayQueue),
    /* tp_itemsize */ 0,
    /* tp_dealloc */ (destructor)ArrayQueue_dealloc,
    /* tp_print */ 0,
    /* tp_getattr */ 0,
    /* tp_setattr */ 0,
    /* tp_reserved */ 0,
    /* tp_repr */ 0,
    /* tp_as_number */ 0,
    /* tp_as_sequence */ 0,
    /* tp_as_mapping */ &ArrayQueue_PyMappingMethods,
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
    /* tp_methods */ ArrayQueue_PyMethodDef,
    /* tp_members */ 0,
    /* tp_getset */ 0,
    /* tp_base */ 0,
    /* tp_dict */ 0,
    /* tp_descr_get */ 0,
    /* tp_descr_set */ 0,
    /* tp_dictoffset */ 0,
    /* tp_init */ 0,
    /* tp_alloc */ 0,
    /* tp_new */ ArrayQueue___new__,
};

#endif // CYGORITHMS_QUEUE_H