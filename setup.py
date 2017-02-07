from setuptools import setup, find_packages

from io import open
from os import path

import dictcomparator

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dictcomparator',
    version=dictcomparator.__version__,

    description=('A simple library for a better dictionary comparison when '
                 'testing code'),
    long_description=long_description,

    url='https://github.com/maccinza/dict_comparator',

    author='Lucas Infante',
    author_email='maccinza@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],

    keywords='testing dict dictionary comparison',

    install_requires=['deepdiff'],

    extras_require={
        'dev': ['nose'],
        'test': ['coverage'],
    },
)
