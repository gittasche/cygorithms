from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

linked_list_name = ".".join(["cygorithms", "linked_list", "cy_linked_list"])
linked_list_source = ["/".join(["cygorithms", "linked_list", "linked_list_src", "cy_linked_list.pyx"])]

linked_list_ext = Extension(
    name=linked_list_name,
    sources=linked_list_source
)

array_name = ".".join(["cygorithms", "arrays", "carray"])
array_sources = ["/".join(["cygorithms", "arrays", "carray_src", "array.c"])]

array_ext = Extension(
    name=array_name,
    sources=array_sources
)

__version__ = "0.0.1"

setup(
    name="cygorithms",
    version=__version__,
    description="Algorithms written on Cython",
    author="gittasche",
    python_requires=">=3.9",
    install_requires=["Cython>=0.29.32"],
    packages=find_packages(),
    ext_modules=cythonize([array_ext, linked_list_ext]),
    zip_safe=False
)