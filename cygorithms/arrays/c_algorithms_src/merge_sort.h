#ifndef CYGORITHMS_MERGE_SORT_H
#define CYGORITHMS_MERGE_SORT_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <stddef.h>
#include <math.h>
#include "../c_array_src/onedarray.h"
#include "../c_array_src/dynonedarray.h"
#include "../c_util/util.h"

static int merge_impl(PyObject *array, PyObject *comp, size_t bl, size_t el, size_t br, size_t er, size_t end)
{
    size_t i, j, k;
    size_t n_left = el - bl;
    size_t n_right = er - br;
    size_t init_left = 0, init_right = 0;

    PyObject *Py_i, *Py_j, *Py_k;

    PyObject **array_left = (PyObject**)malloc(n_left * sizeof(PyObject*));
    PyObject **array_right = (PyObject**)malloc(n_right * sizeof(PyObject*));

    for (i = bl; i < el; ++i)
    {
        if (i < end)
        {
            Py_i = PyLong_FromSize_t(i);
            array_left[i - bl] = PyObject_GetItem(array, Py_i);
            init_left++;
        }
    }
    for (j = br; j < er; ++j)
    {
        if (j < end)
        {
            Py_j = PyLong_FromSize_t(j);
            array_right[j - br] = PyObject_GetItem(array, Py_j);
            init_right++;
        }
    }

    i = 0;
    j = 0;
    k = bl;
    while (i < init_left && j < init_right)
    {
        Py_k = PyLong_FromSize_t(k);
        if (_comp(array_left[i], array_right[j], comp) == 1)
        {
            PyObject_SetItem(array, Py_k, array_left[i]);
            i++;
        }
        else
        {
            PyObject_SetItem(array, Py_k, array_right[j]);
            j++;
        }
        k++;
    }
    
    for ( ; i < init_left; ++i)
    {
        Py_k = PyLong_FromSize_t(k);
        PyObject_SetItem(array, Py_k, array_left[i]);
        k++;
    }
    for ( ; j < init_right; ++j)
    {
        Py_k = PyLong_FromSize_t(k);
        PyObject_SetItem(array, Py_k, array_right[j]);
        k++;
    }

    free(array_left);
    free(array_right);
    return 0;
}

static PyObject* merge_sort_impl(PyObject *array, PyObject *comp, size_t begin, size_t end)
{
    size_t size, pow_2, i;
    for (size = 0; size < floor(log2(end - begin)) + 1; ++size)
    {
        pow_2 = pow(2, size);
        i = begin;
        while (i < end)
        {
            merge_impl(array, comp, i, i + pow_2, i + pow_2, i + 2 * pow_2, end);
            i = i + 2 * pow_2;
        }
    }
    return array;
}

static PyObject* merge_sort(PyObject *self, PyObject *args, PyObject *kwds)
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

    args0 = merge_sort_impl(args0, comp, begin, end);
    if (is_DynamicOneDArray)
        PyObject_CallMethod(args0, "_modify", "O", Py_True);

    Py_INCREF(args0);
    return args0;
}

#endif // CYGORITHMS_MERGE_SORT_H