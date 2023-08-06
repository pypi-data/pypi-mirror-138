# -*- coding: utf-8-

"""Test the console_test module, without the test_oemof function
"""
import unittest
from oemof.solph import console_scripts

class TestSolphConsoleScripts(unittest.TestCase):

    def test_console_scripts(self):
        console_scripts.check_oemof_installation(silent=False)
