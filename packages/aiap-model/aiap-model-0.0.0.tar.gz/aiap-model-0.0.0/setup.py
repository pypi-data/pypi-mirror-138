#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'aiap-model'
DESCRIPTION = "Example classification model package from AIAP assessment."
URL = "https://github.com/ChngYuanLongRandy/AIAP"
EMAIL = "chngyuanlong@gmail.com"
AUTHOR = "Randy Chng"
REQUIRES_PYTHON = "==3.10.0"
VERSION = "0.0.0"

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the
# Trove Classifier for that!

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Load the package's VERSION file as a dictionary.
# about = {}
# ROOT_DIR = Path(__file__).resolve().parent
# REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
# PACKAGE_DIR = ROOT_DIR / 'regression_model'
# with open(PACKAGE_DIR / "VERSION") as f:
#     _version = f.read().strip()
#     about["__version__"] = _version


# What packages are required for this module to be executed?
def list_reqs(fname="requirements.txt"):
    with open(fname) as fd:
        return fd.read().splitlines()

# Where the magic happens:
setup(
    name=NAME,
    version= VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    # will not include any packages found in test folder
    packages=find_packages(exclude=("test",)),
    # package_data={"regression_model": ["VERSION"]},
    install_requires=list_reqs(),
    extras_require={},
    include_package_data=True,
    license="BSD-3",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)