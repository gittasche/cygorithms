#include <Python.h>
#include "select_sort.h"

static PyMethodDef algorithms_PyMethodDef[] = {
    {"selection_sort", (PyCFunction)selection_sort,
     METH_VARARGS | METH_KEYWORDS, ""},
    {NULL, NULL, 0, NULL}   /* Sentinel */
};

static struct PyModuleDef algorithms_struct = {
    PyModuleDef_HEAD_INIT,
    "c_algorithms",
    0,
    -1,
    algorithms_PyMethodDef
};

PyMODINIT_FUNC PyInit_c_algorithms(void)
{
    Py_Initialize();
    PyObject *c_algorithms = PyModule_Create(&algorithms_struct);
    return c_algorithms;
}
