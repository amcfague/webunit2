import unittest

import webunit2.framework
import webunit2.response

from inspect import getmembers, ismethod


def method_maker(action, asserter):
    """ ROAR """
    def _wrapper(self, *args, **kwargs):
        resp = eval("self.%s" % action)
        assertion = eval("resp.%s" % asserter)
        if not assertion:
            raise AssertionError()
        return assertion
    return _wrapper


class AssertionMaker(type):


    def __new__(cls, name, bases, attrs):
        def pred(func):
            return ismethod(func) and func.func_name.startswith("assert")

        docstring = """
Alias for :meth:`~webunit2.framework.Framework.{action}` .
:meth:`~webunit2.response.HttpResponse.{assertion}`.
        """
        actions = ['delete', 'get', 'post', 'put']
        callables = dict(getmembers(webunit2.response.HttpResponse, pred))

        for action in actions:
            for meth_name, meth in callables.items():
                new_meth_name = "{action}_{meth_name}".format(
                    action=action, meth_name=meth_name)
                new_meth = method_maker(action, meth_name)
                new_meth.__doc__ = docstring.format(
                    action=action, assertion=meth_name) 
                attrs[new_meth_name] = new_meth

        return type.__new__(cls, name, bases, attrs)



class TestCase(webunit2.framework.Framework, unittest.TestCase):
    """
    Basic wrapper around :class:`~webunit2.framework.Framework` that implements
    :class:`unittest.TestCase` and adds a variety of assertion methods.
    """

    __metaclass__ = AssertionMaker

    def __init__(self, methodName='runTest', url=None):
        unittest.TestCase.__init__(self, methodName=methodName)
        webunit2.framework.Framework.__init__(self, url=url)
