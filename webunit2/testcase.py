import unittest

import webunit2.framework


class TestCase(unittest.TestCase, webunit2.framework.Framework):
    """
    Basic wrapper around :class:`~webunit2.framework.Framework` that implements
    :class:`unittest.TestCase` and adds a variety of assertion methods.
    """

    def __init__(self, url=None):
        webunit2.framework.Framework.__init__(self, url)
