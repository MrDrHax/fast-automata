from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
import sys, os
import setuptools

__version__ = '0.3.0'

using_pybind = False

try:
    from fastautomata import fastautomata_clib

except ImportError:
    print("Could not import fastautomata_clib, please install pybind11 and a compiler to compile liraries. Attempting to compile")

    import pybind11

    def get_pybind_include(user=False):
        return pybind11.get_include(user)



    # Define Pybind11 extension
    ext_modules = [
        Extension(
            'fastautomata.fastautomata_clib',
            ['fastautomata/include/fastautomata/bindings.cpp'],
            include_dirs=[
                # Path to pybind11 headers
                get_pybind_include(),
                get_pybind_include(user=True),
            ],
            language='c++'
        ),
    ]

    using_pybind = True

setup(
    name="fast-automata",
    version=__version__,
    packages=find_packages(),
    author="Alejandro Fernandez",
    author_email="alexfh2001@gmail.com",
    description="A 'fast' library for cellular automata simulations. I was just done with mesa and it's confusing/restrictive api.",
    package_data={
        '': ['*.pyi'],  # Include all .pyi files
        'fastautomata': ['fastautomata_clib.*'],  # Include specific .pyi file
    },
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MrDrHax/fast-automata",
    install_requires=["pyglet", "pydantic", "fastapi", "uvicorn", "pybind11"],
    python_requires='>=3.10',
    license="GPLv3",
    ext_modules = ext_modules if using_pybind else None,
)