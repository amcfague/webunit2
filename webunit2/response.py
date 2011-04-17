import webunit2.utils

class HttpResponse(object):
    """
    Creates an object out of the :class:`httplib2.Response`, which is just a
    subclass of dict.  Since we want to make the response a little easier to
    deal with, this class will objectify it.

    ``response``:
        dictionary like object returned from an :class:`httplib2` request.
    ``content``:
        Content returned in the body of the response.
    """
    def __init__(self, response, content=""):
        self.status = "%d %s" % (response.status, response.reason)
        self.status_int = response.status
        self.status_reason = response.reason

        self.content_type = response.get('content-type')
        self.cookies = webunit2.utils.parse_cookies(response.get('set-cookie'))
        self.body = content

        self.raw_headers = dict(response)

    def assertInBody(self, content):
        """
        Returns `True` if ``content`` appears in the body of the response,
        `False` if not.
        """
        return content in self.body

    def assertNotInBody(self, content):
        return not self.assertInBody(content)

    def assertStatus(self, status):
        """
        Returns `True` if ``status`` was the status code received by this
        response, `False` if not.
        """
        return status == self.status_int

    def assertNotStatus(self, status):
        return not self.assertStatus(status)

    def assertHeader(self, name, value=None):
        """
        Returns `True` if ``name`` was in the headers and, if ``value`` is
        True, whether or not the values match, or `False` otherwise.
        """
        return name in self.raw_headers and (
            True if value is None else self.raw_headers[name] == value)

    def assertNotHeader(self, name, value=None):
        return not self.assertHeader(name, value)
    
    def assertCookie(self, name, value=None, attrs={}):
        """
        Returns `True` if:

            - the cookie name appears in the response
            - if value is not None, the values are equal
            - if any of the attributes match

        For example, to check to see if the HttpOnly and path attribute are set::

            assertCookie("cookie_name", attrs={'HttpOnly': True, "Path": "/"})
        """
        name = name.lower()
        if name not in self.cookies:
            return False
        if value is not None and self.cookies[name][name] != value:
            return False

        cookie = self.cookies[name]
        for k, v in attrs.items():
            k = k.lower()
            if k not in cookie or cookie[k] != v:
                return False

        return True

    def assertNotCookie(self, name, value=None, attrs={}):
        return not self.assertCookie(name, value, attrs)
