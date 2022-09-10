from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize

__name__ = "cygorithms"
__version__ = "0.0.1"

def __get_array_ext():
    array_name = ".".join([__name__, "arrays", "c_array"])
    array_sources = [
        "/".join([__name__, "arrays", "c_array_src", "array.c"])
    ]

    array_ext = Extension(
        name=array_name,
        sources=array_sources
    )

    algorithms_name = ".".join([__name__, "arrays", "c_algorithms"])
    algorithms_sources = [
        "/".join([__name__, "arrays", "c_algorithms_src", "algorithms.c"])
    ]

    algorithms_ext = Extension(
        name=algorithms_name,
        sources=algorithms_sources
    )

    array_ext_full = [array_ext, algorithms_ext]

    return array_ext_full

def __get_linked_list_ext():
    linked_list_name = ".".join([__name__, "linked_list", "cy_linked_list"])
    linked_list_sources = [
        "/".join([__name__, "linked_list", "cy_linked_list_src", "cy_linked_list.pyx"])
    ]

    linked_list_ext = Extension(
        name=linked_list_name,
        sources=linked_list_sources
    )

    linked_list_ext_full = [linked_list_ext]

    return linked_list_ext_full

def __get_trees_ext():
    trees_name = ".".join([__name__, "trees", "cy_trees"])
    trees_sources = ["/".join([__name__, "trees", "cy_trees_src", "cy_binary_tree.pyx"])]

    trees_ext = Extension(
        name=trees_name,
        sources=trees_sources
    )

    trees_ext_full = [trees_ext]

    return trees_ext_full

__extensions = []

__extensions.extend(__get_array_ext())
__extensions.extend(__get_linked_list_ext())
__extensions.extend(__get_trees_ext())

setup(
    name=__name__,
    version=__version__,
    description="Algorithms written on Cython",
    author="gittasche",
    python_requires=">=3.9",
    install_requires=["Cython>=0.29.32"],
    packages=find_packages(),
    ext_modules=cythonize(__extensions),
    zip_safe=False
)
