:mod:`webunit2.testcase`
------------------------

.. autoclass:: webunit2.testcase.TestCase
    :members:
    :undoc-members:
    
    All assertion wrappers take the form of ``{action}_{assertion}``.  Each one
    contains a link to the respective documentation, but to get a general,
    cleaner overview may be simpler to just look at the documentation for the
    :class:`~webunit2.response.HttpResponse` class.  Any methods beginning with
    `assert` will work.  That is::

        get_assertCookie()

    ...will call :meth:`~webunit2.framework.Framework.get`, and then call the
    :meth:`~webunit2.response.HttpResponse.assertCookie` method on the
    response.
