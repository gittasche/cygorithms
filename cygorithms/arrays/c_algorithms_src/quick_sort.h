#ifndef CYGORITHMS_QUICK_SORT_H
#define CYGORITHMS_QUICK_SORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <stddef.h>
#include "../c_array_src/onedarray.h"
#include "../c_array_src/dynonedarray.h"
#include "../c_util/util.h"

static size_t partition(PyObject *array, PyObject *comp, size_t begin, size_t end)
{
    PyObject *x = PyObject_GetItem(array, PyLong_FromSize_t(end));
    size_t piv = begin;

    PyObject *Py_piv, *Py_i;

    for (size_t i = begin; i < end; ++i)
    {
        Py_i = PyLong_FromSize_t(i);
        if (_comp(PyObject_GetItem(array, Py_i), x, comp) == 1)
        {
            Py_piv = PyLong_FromSize_t(piv);
            PySwap_ArrayItems(array, Py_piv, Py_i);
            piv++;
        }
    }

    Py_piv = PyLong_FromSize_t(piv);
    PySwap_ArrayItems(array, Py_piv, PyLong_FromSize_t(end));
    return piv;
}

static PyObject *quick_sort_impl(PyObject *array, PyObject *comp, size_t begin, size_t end)
{
    size_t *stack = (size_t*)malloc((end - begin) * sizeof(size_t));

    size_t top = 0;
    
    stack[top++] = begin;
    stack[top++] = end - 1;

    while (top > 0)
    {
        end = stack[--top];
        begin = stack[--top];

        size_t piv = partition(array, comp, begin, end);

        if (piv > begin + 1)
        {
            stack[top++] = begin;
            stack[top++] = piv - 1;
        }

        if (piv + 1 < end)
        {
            stack[top++] = piv + 1;
            stack[top++] = end;
        }
    }
    return array;
}

static PyObject *quick_sort(PyObject *self, PyObject *args, PyObject *kwds)
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

    args0 = quick_sort_impl(args0, comp, begin, end);
    if (is_DynamicOneDArray)
        PyObject_CallMethod(args0, "_modify", "O", Py_True);

    Py_INCREF(args0);
    return args0;
}

#endif // CYGORITHMS_QUICK_SORT_H
