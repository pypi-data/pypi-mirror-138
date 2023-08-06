# -*- coding: utf-8 -
"""Regression tests.
"""
from nose.tools import ok_
import vppopt

def test_version_metadata():
    ok_(vppopt.__version__)