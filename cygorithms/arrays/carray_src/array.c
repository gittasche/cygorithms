#include <Python.h>
#include "array.h"
#include "onedarray.h"
#include "dynarray.h"
#include "dynonedarray.h"

static struct PyModuleDef array_struct = {
    PyModuleDef_HEAD_INIT,
    "carray",
    0,
    -1,
    NULL
};

PyMODINIT_FUNC PyInit_carray(void)
{
    Py_Initialize();
    PyObject *carray = PyModule_Create(&array_struct);
    
    if (PyType_Ready(&ArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&ArrayType);
    PyModule_AddObject(carray, "Array", (PyObject*)(&ArrayType));

    if (PyType_Ready(&OneDArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&OneDArrayType);
    PyModule_AddObject(carray, "OneDArray", (PyObject*)(&OneDArrayType));

    if (PyType_Ready(&DynamicArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&ArrayType);
    PyModule_AddObject(carray, "DynamicArray", (PyObject*)(&DynamicArrayType));

    if (PyType_Ready(&DynamicOneDArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&DynamicOneDArrayType);
    PyModule_AddObject(carray, "DynamicOneDArray", (PyObject*)(&DynamicOneDArrayType));

    return carray;
}