from setuptools import setup, find_packages
from Cython.Build import cythonize

from cygorithms.linked_list._extension import linked_list_ext

extensions = [
    linked_list_ext
]

__version__ = "0.0.1"

setup(
    name="cygorithms",
    version=__version__,
    description="Algorithms written on Cython",
    author="gittasche",
    python_requires=">=3.9",
    install_requires=["Cython>=0.29.32"],
    packages=find_packages(),
    ext_modules=cythonize(extensions),
    zip_safe=False
)