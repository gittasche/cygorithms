#ifndef CYGORITHMS_SELECT_SORT_H
#define CYGORITHNS_SELECT_SORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stddef.h>
#include "../c_array_src/onedarray.h"
#include "../c_array_src/dynonedarray.h"
#include "../c_util/util.h"

static PyObject* selection_sort_impl(PyObject *array, size_t begin, size_t end, PyObject *comp)
{
    long i, j, min_idx;
    PyObject *Py_min_idx, *Py_j, *Py_i;
    for (i = begin; i < end - 1; ++i)
    {
        min_idx = i;
        for (j = i + 1; j < end; ++j)
        {
            Py_min_idx = PyLong_FromLong(min_idx);
            Py_j = PyLong_FromSize_t(j);
            if (_comp(PyObject_GetItem(array, Py_j), PyObject_GetItem(array, Py_min_idx), comp) == 1)
                min_idx = j;
        }
        if (min_idx != i)
        {
            Py_min_idx = PyLong_FromLong(min_idx);
            Py_i = PyLong_FromLong(i);
            PySwap_ArrayItems(array, Py_min_idx, Py_i);
        }
    }
    return array;
}

static PyObject* selection_sort(PyObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *args0 = NULL, *comp = NULL;
    PyObject *Py_begin = NULL, *Py_end = NULL;
    size_t begin, end;

    args0 = PyObject_GetItem(args, PyLong_FromLong(0));
    int is_OneDArray = _check_type(args0, &OneDArrayType);
    int is_DynamicOneDArray = _check_type(args0, &DynamicOneDArrayType);
    if (!is_OneDArray && !is_DynamicOneDArray)
    {
        raise_exception_if_not_array(args0);
        return NULL;
    }

    comp = PyObject_GetItem(kwds, PyUnicode_FromString("comp"));
    if (comp == NULL)
        PyErr_Clear();

    Py_begin = PyObject_GetItem(kwds, PyUnicode_FromString("begin"));
    if (Py_begin == NULL)
    {
        PyErr_Clear();
        begin = 0;
    }
    else
        begin = PyLong_AsSize_t(Py_begin);

    Py_end = PyObject_GetItem(kwds, PyUnicode_FromString("end"));
    if (Py_end == NULL)
    {
        PyErr_Clear();
        end = PyObject_Length(args0);
    }
    else
        end = PyLong_AsSize_t(Py_end);

    args0 = selection_sort_impl(args0, begin, end, comp);

    if (is_DynamicOneDArray)
        PyObject_CallMethod(args0, "_modify", "O", Py_True);

    Py_INCREF(args0);
    return args0;
}

#endif // CYGORITHNS_SELECT_SORT_H