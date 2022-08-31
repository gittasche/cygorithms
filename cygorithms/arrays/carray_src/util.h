#ifndef CYGORITHMS_UTIL_H
#define CYGORITHMS_UTIL_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>

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

#endif // CYGORITHMS_UTIL_H