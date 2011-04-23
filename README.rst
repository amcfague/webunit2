``webunit2`` is a spiritual successor to `Richard Jones' webunit
<http://mechanicalcat.net/tech/webunit/>`_, but is by no means a fork.  This
library has been built from the ground up, complete with documentation and
testing.  It's also `hosted on GitHub <https://github.com/amcfague/webunit2>`_,
making it a cinch to fork.

Documentation
-------------

`Documentation is available on PyPi. <http://packages.python.org/webunit2/>`_.

You can also build the documentation yourself.  Make sure Sphinx is installed
by running::

    $ easy_install -U sphinx

Then, clone the repository, `cd` into it, and run::

    $ python setup.py build_sphinx

Documentation is available in ``build/sphinx/html``.

Getting Started
---------------

Getting started is really, really easy.  All you need to do is implement
``webunit2.testcase.Testcase`` and start writing unit tests. ::

    import webunit2

    class TestMyApp(webunit2.TestCase):

        def __init__(self):
            # You aren't required to initialize the base class here, but it
            # makes dealing with subsequent requests easier--because they can
            # be relative paths!
            webunit2.TestCase.__init__(self, "http://myapp.com")

        def test_some_url(self):
            # Just do a normal get
            self.get('/somepath')

            # Lets post some data
            self.post('/somepath', post_params={"key": "value"})

            # No helper function for your HTTP method?  No problem!
            self.make_request("HEAD", "/somepath")

Of course, because this is a unit testing framework, you'll probably be making
a lot of assertions--especially in content.  That's easy too! ::

        def test_for_content(self):
            # Assert the word `hippo` appears in the content.
            self.get_assertContent('/something', content="hippo")
            # Assert that the `X-Customheader` header was set.
            self.get_assertHeader('/something', 'X-Customheader')

If either of these fail (i.e., the return code is not 200 or the content does
not contain `hippo`), an ``AssertionError`` is raised as normal.  And of
course, if you need to check for multiple values on the response, the same
``assert*`` functions are available directly on the response.  For example, the
above could be rewritten as::

        def test_for_content_resp(self):
            resp = self.get('/something')
            # Assert the word `hippo` appears in the content.
            resp.assertContent("hippo")
            # Assert that the `X-Customheader` header was set.
            resp.assertHeader('X-Customheader')

This also allows you to chain many more assertions together--i.e., checking for
headers, cookies, etc..  These were *all* designed to make testing easier, so
if you have suggestions or complaints...

Contributing
------------

The source code is `hosted on Github <https://github.com/amcfague/webunit2>`_,
which makes it a cinch to fork and contribute.  `Please submit issues using the
GitHub tracker <https://github.com/amcfague/webunit2/issues>`_!  I love getting
feedback, and I urge you to file tickets for features and/or bugs.
