import unittest
import webunit2.framework

class TestCase(unittest.TestCase, webunit2.framework.Framework):

    def __init__(self, url=None):
        webunit2.framework.Framework.__init__(self, url)
