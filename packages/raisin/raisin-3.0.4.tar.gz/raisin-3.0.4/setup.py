#!/usr/bin/env python3

"""
** Configuration file for pypi. **
----------------------------------

#!/bin/bash

python3 setup.py check -s -r
python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel
python3 -m pip install --user --upgrade twine
python3 -m twine upload --repository pypi dist/*
twine check dist/*
"""

import setuptools

import raisin

with open('README.rst', 'r', encoding='utf-8') as file:
    long_description = file.read()

setuptools.setup(
    name='raisin',
    version=raisin.__version__,
    author='Robin RICHARD (robinechuca)',
    author_email='raisin@ecomail.fr',
    description='Simple parallel, distributed and cluster computing',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://framagit.org/robinechuca/raisin/-/blob/master/README.rst',
    packages=setuptools.find_packages(),
    install_requires=['dill', 'context-verbose'],
    extras_require={
        'tests': ['pytest'],
        'documentation': ['pdoc3', 'pyreverse'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        # 'Natural Language :: French',
        # 'Operating System :: MacOS',
        # 'Operating System :: Microsoft :: Windows',
        # 'Operating System :: POSIX :: BSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Clustering',
        'Topic :: Internet',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: System :: Power (UPS)'],
    keywords=[
        'parallel',
        'parallelisation',
        'distributed',
        'cluster work',
        'cluster computing',
        'serialization',
        'serialize'
        'client',
        'server'],
    python_requires='>=3.6',
    project_urls={
        'Source Repository': 'https://framagit.org/robinechuca/raisin',
        # 'Bug Tracker': 'https://github.com/engineerjoe440/ElectricPy/issues',
        'Documentation': 'http://raisin-docs.ddns.net',
        # 'Packaging tutorial': 'https://packaging.python.org/tutorials/distributing-packages/',
        },
    include_package_data=True,
)
