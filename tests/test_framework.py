import base64
import unittest
import urllib

from mock import patch

from webunit2 import Framework


class TestFramework(unittest.TestCase):

    def test_init_url(self):
        """ Test that protocol and server are set correctly with given URL """
        fw = Framework("https://google.com:443")
        self.assertEqual(fw.protocol, "https")
        self.assertEqual(fw.server, "google.com:443")

    def test_init_bad_url(self):
        """ Test that init raises an Exception with a bad URL """
        self.assertRaises(Exception, Framework, "bad_url")

    def test_init_no_url(self):
        """ Test that protocol and server are set correctly with no URL """
        fw = Framework()
        self.assertIsNone(fw.protocol)
        self.assertIsNone(fw.server)

    def test_prepare_basic_auth(self):
        """ Test that passing in a username and password returns a string """
        username, password = "user", "pass"
        auth_str = base64.b64encode(":".join((username, password)))

        fw = Framework()
        header_key, header_value = fw._prepare_basicauth(username, password)

        self.assertEquals(header_key, "Authorization")
        self.assertEquals(header_value, "Basic %s" % auth_str)

    def test_prepare_basic_auth_no_password(self):
        """ Test that basic auth fails with username and no password """
        fw = Framework()
        self.assertRaises(Exception, fw._prepare_basicauth, "username", None)

    def test_prepare_basic_auth_no_username(self):
        """ Test that basic auth fails with password and no username """
        fw = Framework()
        self.assertRaises(Exception, fw._prepare_basicauth, None, "password")

    def test_prepare_basic_auth_no_info(self):
        """ Test that basic auth returns None with no username or password """
        fw = Framework()
        self.assertIsNone(fw._prepare_basicauth(None, None))

    def test_prepare_uri_relative_url_no_query(self):
        """ Test that relative URLs get generated correctly with no query param """
        base_url = "https://someurl:443"
        path = "/something"
        expected_uri = "".join((base_url, path))

        fw = Framework(base_url)
        self.assertEqual(fw._prepare_uri(path), expected_uri)

    def test_prepare_uri_relative_url_with_query(self):
        """ Test that relative URLs get generated correctly with a query param """
        base_url = "https://someurl:443"
        path = "/something"
        query_params = {"key1": "val1", "key2": "val2"}
        expected_uri = "".join((base_url, path)) + "?" + urllib.urlencode(query_params, True)


        fw = Framework(base_url)
        self.assertEqual(fw._prepare_uri(path, query_params), expected_uri)

    def test_prepare_uri_absolute_url_no_query(self):
        """ Test that absolute URLs get generated correctly with no query param """
        path = "http://www.baseurl.com/something"

        fw = Framework()
        self.assertEqual(fw._prepare_uri(path), path)

    def test_prepare_uri_absolute_url_with_query(self):
        """ Test that absolute URLs get generated correctly with query param """
        path = "http://www.baseurl.com/something"
        query_params = {"key1": "val1", "key2": "val2"}
        expected_uri = path + "?" + urllib.urlencode(query_params, True)

        fw = Framework()
        self.assertEqual(fw._prepare_uri(path, query_params), expected_uri)


    @patch("httplib2.Http.request")
    def test_make_request_basic_auth(self, mock_request):
        """ Test that a basic auth request generates the correct header """
        path = "http://google.com"
        username, password = "user", "pass"
        auth_str = base64.b64encode(":".join((username, password)))
        expected_uri = path
        expected_headers = {"Authorization": "Basic %s" % auth_str}

        mock_request.return_value = {'status': 200}, ""

        fw = Framework()
        fw.make_request("GET", path, username=username, password=password)
        mock_request.asserted_called_with(expected_uri, method="GET",
                                          body=None, headers=expected_headers)

    @patch("httplib2.Http.request")
    def test_make_request_params_non_post(self, mock_request):
        """ Test that non-POST post params get set as a query string """
        path = "http://google.com"
        post_params = {"key1": "val1"}
        expected_uri = "?".join((path, urllib.urlencode(post_params)))

        mock_request.return_value = {'status': 200}, ""

        fw = Framework()
        fw.make_request("GET", path, post_params=post_params)
        mock_request.asserted_called_with(expected_uri, method="GET",
                                          body=None, headers=None)


    @patch("webunit2.framework.Framework.make_request")
    def test_delete(self, mock_make_request):
        """ Test that a DELETE calls make_request with the correct parameters """
        fw = Framework()
        fw.delete()
        mock_make_request.assert_called_with("DELETE")

    @patch("webunit2.framework.Framework.make_request")
    def test_get(self, mock_make_request):
        """ Test that a GET calls make_request with the correct parameters """
        fw = Framework()
        fw.get()
        mock_make_request.assert_called_with("GET")

    @patch("webunit2.framework.Framework.make_request")
    def test_get(self, mock_make_request):
        """ Test that a POST calls make_request with the correct parameters """
        fw = Framework()
        fw.post()
        mock_make_request.assert_called_with("POST")

    @patch("webunit2.framework.Framework.make_request")
    def test_put(self, mock_make_request):
        """ Test that a PUT calls make_request with the correct parameters """
        fw = Framework()
        fw.put()
        mock_make_request.assert_called_with("PUT")
