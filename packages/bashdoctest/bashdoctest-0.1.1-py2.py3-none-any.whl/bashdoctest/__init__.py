# -*- coding: utf-8 -*-
'''
'''

from __future__ import absolute_import
from bashdoctest.core import Runner

__author__ = """Michael Delgado, Julian Edwards"""
__version__ = '0.1.1'

_module_imports = (
    Runner,
)

__all__ = list(map(lambda x: x.__name__, _module_imports))
