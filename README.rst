``webunit2`` is a spiritual successor to `Richard Jones' webunit
<http://mechanicalcat.net/tech/webunit/>`_, but is by no means a fork.  This
library has been built from the ground up, complete with documentation and
testing.  It's also `hosted on GitHub <https://github.com/amcfague/webunit2>`_,
making it a cinch to fork.


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
            self.get_assertStatus('/something', status=200)
            self.get_assertContent('/something', content="hippo")

            # Or do both in the same step
            self.get_assert('/something', status=200, content="hippo")

If either of these fail (i.e., the return code is not 200 or the content does
not contain `hippo`), an ``AssertionError`` is raised as normal.

Contributing
------------

The source code is `hosted on Github <https://github.com/amcfague/webunit2>`_,
which makes it a cinch to fork and contribute.
