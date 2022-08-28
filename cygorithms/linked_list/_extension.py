from setuptools import Extension

linked_list_ext = Extension(
    name = "cygorithms.linked_list.cy_linked_list",
    sources=["cygorithms/linked_list/cy_linked_list.pyx"]
)
