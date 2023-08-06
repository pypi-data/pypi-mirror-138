import os
from setuptools import Extension, setup
from Cython.Build import cythonize
from Cython.Compiler import Options
import numpy

for file in os.listdir():
    if "filter" in file and ".pyx" in file:
        factor_name= file.split('.pyx')[0]

        ext_modules = [
            Extension(
                factor_name,
                [factor_name+".pyx"],
                extra_compile_args=['/openmp'],
            )
        ]

        setup(
            name=factor_name,
            ext_modules=cythonize(ext_modules,
                                language_level='3',
                                compiler_directives={'boundscheck': False,
                                                    'wraparound': False,
                                                    'infer_types': True,
                                                    'initializedcheck': False,
                                                    'linetrace': False,}),
            include_dirs=[numpy.get_include()],
        )