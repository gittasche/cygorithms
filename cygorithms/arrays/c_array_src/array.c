#include <Python.h>
#include "array.h"
#include "onedarray.h"
#include "dynarray.h"
#include "dynonedarray.h"
#include "stack.h"
#include "queue.h"

static struct PyModuleDef array_struct = {
    PyModuleDef_HEAD_INIT,
    "c_array",
    0,
    -1,
    NULL
};

PyMODINIT_FUNC PyInit_c_array(void)
{
    Py_Initialize();
    PyObject *c_array = PyModule_Create(&array_struct);
    
    if (PyType_Ready(&ArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&ArrayType);
    PyModule_AddObject(c_array, "Array", (PyObject*)(&ArrayType));

    if (PyType_Ready(&OneDArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&OneDArrayType);
    PyModule_AddObject(c_array, "OneDArray", (PyObject*)(&OneDArrayType));

    if (PyType_Ready(&DynamicArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&ArrayType);
    PyModule_AddObject(c_array, "DynamicArray", (PyObject*)(&DynamicArrayType));

    if (PyType_Ready(&DynamicOneDArrayType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&DynamicOneDArrayType);
    PyModule_AddObject(c_array, "DynamicOneDArray", (PyObject*)(&DynamicOneDArrayType));

    if (PyType_Ready(&ArrayStackType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&ArrayStackType);
    PyModule_AddObject(c_array, "ArrayStack", (PyObject*)(&ArrayStackType));

    if (PyType_Ready(&ArrayQueueType) < 0)
    {
        return NULL;
    }
    Py_INCREF(&ArrayQueueType);
    PyModule_AddObject(c_array, "ArrayQueue", (PyObject*)(&ArrayQueueType));

    return c_array;
}