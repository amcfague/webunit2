import base64
import logging
import urllib
import urlparse

import httplib2
import poster.encode

from webunit2.response import HttpResponse
from webunit2.utils import parse_url


log = logging.getLogger(__name__)


class Framework(object):
    """
    This is a basic framework to automate interacting with any web service.  It
    is intended to be used for integration testing, but in all reality, it can
    be used for anything that is consistantly making requests.

    ``url``:
        A full URL with protocol included.  If the service is running on a
        non-standard port, it should be included as part of the URL::

            http://someurl.com
            https://super-service.com:123

        URLs containing additional information (such as paths) will have it
        stripped::

            http://something.com:8080/alternative/base

        ...would become::

            http://something.com:8080

        Invalid URLs will raise an assertion error.
    """

    def __init__(self, url=None):
        self._httpobj = httplib2.Http()

        # Force 4xx/5xx httplib exceptions to be ignored
        self._httpobj.force_exception_to_status_code = True

        self.protocol, self.server = parse_url(url) if url else (None, None)

    def _prepare_basicauth(self, username, password):
        """
        Handles BasicAuth preparation and error handling.  Either both
        ``username`` and ``password`` must be defined, or neither.  Defining
        one but not the other will result in an :class:`AssertionError`.

        ``username``
        ``password``

        Returns a tuple of ``(header_key, header_value)`` which can be inserted
        into the headers dictionary.
        """
        if username and password:
            enc_str = base64.b64encode(":".join((username, password)))
            return ("Authorization", "Basic %s" % enc_str)
        elif username or password:
            raise Exception("Username and password must both be specified.")
        else:
            return None

    def _prepare_uri(self, path, query_params={}):
        """
        Prepares a full URI with the selected information.

        ``path``:
            Path can be in one of two formats:

                - If :attr:`server` was defined, the ``path`` will be appended
                  to the existing host, or
                - an absolute URL
        ``query_params``:
            Used to generate a query string, which will be appended to the end
            of the absolute URL.

        Returns an absolute URL.
        """
        query_str = urllib.urlencode(query_params)

        # If we have a relative path (as opposed to a full URL), build it of
        # the connection info
        if path.startswith('/') and self.server:
            protocol = self.protocol
            server = self.server
        else:
            protocol, server, path, _, _, _ = urlparse.urlparse(path)
            assert server, "%s is not a valid URL" % path

        return urlparse.urlunparse((
            protocol, server, path, None, query_str, None))

    def _make_request(self, uri, method, body, headers={}):
        """
        Wraps the response and content returned by :mod:`httplib2` into a
        :class:`~webunit2.response.HttpResponse` object.

        ``uri``:
            Absolute URI to the resource.
        ``method``:
            Any supported HTTP methods defined in :rfc:`2616`.
        ``body``:
            In the case of POST and PUT requests, this can contain the contents
            of the request.
        ``headers``:
            Dictionary of header values to be sent as part of the request.

        Returns a :class:`~webunit2.response.HttpResponse` object containing
        the request results.
        """
        response, content = self._httpobj.request(
            uri, method=method, body=body, headers=headers)

        return HttpResponse(response, content)

    def retrieve_page(self, method, path, post_params={}, headers={},
                      status=200, username=None, password=None,
                      *args, **kwargs):
        """
        Makes the actual request.  This will also go through and generate the
        needed steps to make the request, i.e. basic auth.

        ``method``:
            Any supported HTTP methods defined in :rfc:`2616`.
        ``path``:
            Absolute or relative path. See :meth:`_prepare_uri` for more
            detail.
        ``post_params``:
            Dictionary of key/value pairs to be added as `POST` parameters.
        ``headers``:
            Dictionary of key/value pairs to be added to the HTTP headers.
        ``status``:
            Will error out if the HTTP status code does not match this value.
            Set this to `None` to disable checking.
        ``username``, ``password``:
            Username and password for basic auth; see
            :meth:`_prepare_basicauth` for more detail.

        An important note is that when ``post_params`` is specified, its
        behavior depends on the ``method``.  That is, for `PUT` and `POST`
        requests, the dictionary is multipart encoded and put into the body of
        the request.  For everything else, it is added as a query string to the
        URL.
        """
        # Copy headers so that making changes here won't affect the original
        headers = headers.copy()

        # Update basic auth information
        basicauth = self._prepare_basicauth(username, password)
        if basicauth:
            headers.update([basicauth])

        # If this is a POST or PUT, we can put the data into the body as
        # form-data encoded; otherwise, it should be part of the query string.
        if method in ["PUT", "POST"]:
            datagen, form_hdrs = poster.encode.multipart_encode(post_params)
            body = "".join(datagen)
            headers.update(form_hdrs)
            uri = self._prepare_uri(path)
        else:
            body = ""
            uri = self._prepare_uri(path, post_params)

        # Make the actual request
        response = self._make_request(uri, method, body, headers)

        # Assert that the status we received was expected.
        if status:
            real_status = int(response.status_int)
            assert real_status == int(status), \
                    "expected %s, received %s." % (status, real_status)

        return response

    def delete(self, *args, **kwargs):
        """
        Wrapper around :meth:`make_request`, where ``method`` is `DELETE`.
        """
        return self.retrieve_page("DELETE", *args, **kwargs)

    def get(self, *args, **kwargs):
        """
        Wrapper around :meth:`make_request`, where ``method`` is `GET`.
        """
        return self.retrieve_page("GET", *args, **kwargs)

    def head(self, *args, **kwargs):
        """
        Wrapper around :meth:`make_request`, where ``method`` is `HEAD`.
        """
        return self.retrieve_page("HEAD", *args, **kwargs)

    def post(self, *args, **kwargs):
        """
        Wrapper around :meth:`make_request`, where ``method`` is `POST`.
        """
        return self.retrieve_page("POST", *args, **kwargs)

    def put(self, *args, **kwargs):
        """
        Wrapper around :meth:`make_request`, where ``method`` is `PUT`.
        """
        return self.retrieve_page("PUT", *args, **kwargs)
