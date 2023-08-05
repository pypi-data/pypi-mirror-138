#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    # This duplicates the equivalent in pyproject.toml so that setup.py
    # --version won't report a version of 0.0.0 in editable installs.  setup.py
    # invocations will NOT install build requirements from pyproject.toml.
    # Unfortunately this also causes SetuptoolsDeprecationWarnings to be
    # emitted, complaining about PEP517.
    setup_requires=["setuptools>=60.5.0", "wheel>=0.27", "setuptools-scm>=6.4.2"],
)
