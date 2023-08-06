#!/usr/bin/env python
"""
The setup script.
"""
import os
import io
from setuptools import setup, find_packages
#==============Package meta-data==============#
NAME = 'vppopt'
DESCRIPTION = 'Virtual Power Plant Optimization Platform'
URL = 'https://github.com/cenaero-enb/h2cs-design'
EMAIL = 'vanlong.le@cenaero.be'
AUTHOR = 'Long Le'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.1'
STATUS = "Under development"

# What packages are required for this module to be executed?
REQUIRED = [
    "pyomo==5.7.2",
    "pandas",
    "openpyxl",
    "xlrd",
    "matplotlib",
    "python_jsonschema_objects",
    "xlsxwriter",
    "loguru",
    "oemof.solph",
    "pymoo",
    "xmltodict",
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

here = os.path.abspath(os.path.dirname(__file__))

# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION

setup(
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    description=DESCRIPTION,
    entry_points={
        'console_scripts': ['vppopt=vppopt.interfaces.cli:main'],
    },
    install_requires=REQUIRED,
    license="Apache Software License 2.0",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='vppopt',
    name=NAME,
    packages=find_packages(
        exclude=[
            "tests",
            "*.tests",
            "*.tests.*",
            "tests.*"]
    ),
    setup_requires=[],
    test_suite='tests',
    tests_require=[],
    url=URL,
    version=about['__version__'],    
    #package_data={"":["*.cfg"]},    
    extras_require=EXTRAS,
    zip_safe=False,
)
