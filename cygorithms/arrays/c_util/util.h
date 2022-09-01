#ifndef CYGORITHMS_UTIL_H
#define CYGORITHMS_UTIL_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <string.h>

const char *_encoding = "utf-8";
const char *_invalid_char = "<invalid-character>";

static const char* PyObject_AsString(PyObject *obj)
{
    return PyBytes_AS_STRING(PyUnicode_AsEncodedString(obj, _encoding, _invalid_char));
}

static int set_exception_if_dtype_mismatch(PyObject *value, PyObject *dtype)
{
    if (!PyObject_IsInstance(value, dtype))
    {
        PyErr_WriteUnraisable(
            PyErr_Format(
                PyExc_TypeError,
                "Unable to store %s object in %s type array",
                PyObject_AsString(PyObject_Repr(PyObject_Type(value))),
                PyObject_AsString(PyObject_Repr(dtype))
            )
        );
        return 1;
    }
    return 0;
}

static int raise_exception_if_dtype_mismatch(PyObject *value, PyObject *dtype)
{
    if (!PyObject_IsInstance(value, dtype))
    {
        PyErr_Format(
            PyExc_TypeError,
            "Unable to store %s object in %s type array",
            PyObject_AsString(PyObject_Repr(PyObject_Type(value))),
            PyObject_AsString(PyObject_Repr(dtype))
        );
        return 1;
    }
    return 0;
}

static int PySwap_ArrayItems(PyObject *array, PyObject *index1, PyObject *index2)
{
    PyObject *temp = PyObject_GetItem(array, index1);
    PyObject_SetItem(array, index1, PyObject_GetItem(array, index2));
    PyObject_SetItem(array, index2, temp);
    return 0;
}

static int raise_exception_if_not_array(PyObject *arg)
{
    PyErr_Format(
        PyExc_TypeError,
        "Unable to sort %s data structure. "
        "Expected OneDArray or DynamicOneDArray.",
        PyObject_AsString(PyObject_Repr(PyObject_Type(arg)))
    );
    return 1;
}

static int _check_type(PyObject *arg, PyTypeObject *type)
{
    return strcmp(arg->ob_type->tp_name, type->tp_name) == 0;
}

static int _comp(PyObject *u, PyObject *v, PyObject *tcomp)
{
    int u_isNone = u == Py_None;
    int v_isNone = v == Py_None;
    if (!u_isNone && v_isNone)
        return 1;
    else if (u_isNone && !v_isNone)
        return 0;
    else if (tcomp)
    {
        PyObject *result_PyObject = PyObject_CallFunctionObjArgs(tcomp, u, v, NULL);
        if (!result_PyObject)
        {
            PyErr_Format(
                PyExc_ValueError,
                "Unable to compare %s object with %s object",
                PyObject_AsString(PyObject_Repr(PyObject_Type(u))),
                PyObject_AsString(PyObject_Repr(PyObject_Type(v)))
            );
        }
        return result_PyObject == Py_True;
    }
    else
    {
        int result = PyObject_RichCompareBool(u, v, Py_LE);
        if (result == -1)
        {
            PyErr_Format(
                PyExc_ValueError,
                "Unable to compare %s object with %s object",
                PyObject_AsString(PyObject_Repr(PyObject_Type(u))),
                PyObject_AsString(PyObject_Repr(PyObject_Type(v)))
            );
        }
        return result;
    }
}

#endif // CYGORITHMS_UTIL_H