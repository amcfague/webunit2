import httplib2
import unittest

from mock import MagicMock, Mock, patch

from webunit2.response import HttpResponse


class MockResponse(dict):
    status = 200
    reason = "OK"
    version = 11


class TestResponse(unittest.TestCase):

    def setUp(self):
        mock_response = MockResponse()
        mock_response['set-cookie'] = ""
        mock_response['content-type'] = "text/html"
        self.mock_response = mock_response
    
    @patch("webunit2.utils.parse_cookies", Mock(return_value=None))
    def test_init_no_cookies(self):
        """ Test that basic values get initialized without cookies """
        content = "testing 123"
        resp = HttpResponse(self.mock_response, content)
        self.assertEqual(resp.status_int, self.mock_response.status)
        self.assertEqual(resp.status_reason, self.mock_response.reason)
        self.assertEqual(resp.status, "%d %s" % (
            self.mock_response.status, self.mock_response.reason))
        self.assertEqual(resp.body, content)
        self.assertEqual(resp.content_type, self.mock_response.get('content-type'))
        self.assertEqual(resp.raw_headers, dict(self.mock_response))

    @patch("webunit2.utils.parse_cookies", Mock(return_value=None))
    def test_assert_in_body(self):
        """ Test that objects that appear in the body return True """
        content = "Testing 123"
        resp = HttpResponse(self.mock_response, content)

        self.assertTrue(resp.assertInBody("Testing"))
        self.assertTrue(resp.assertNotInBody("noteventhere"))

        self.assertFalse(resp.assertNotInBody("Testing"))
        self.assertFalse(resp.assertInBody("noteventhere"))

    @patch("webunit2.utils.parse_cookies", Mock(return_value=None))
    def test_assert_status(self):
        """ Test that assertStatus returns True if they match, False otherwise """
        resp = HttpResponse(self.mock_response)
        self.assertTrue(resp.assertStatus(200))
        self.assertTrue(resp.assertNotStatus(400))

        self.assertFalse(resp.assertStatus(400))
        self.assertFalse(resp.assertNotStatus(200))

    @patch("webunit2.utils.parse_cookies", Mock(return_value=None))
    def test_assert_header(self):
        """ Test that checking for headers returns the correct values """
        resp = HttpResponse(self.mock_response)
        self.assertTrue(resp.assertHeader('content-type'))
        self.assertTrue(resp.assertHeader('content-type', 'text/html'))
        self.assertFalse(resp.assertHeader('content-type', 'plain/text'))
        self.assertFalse(resp.assertHeader('not a header'))
        self.assertFalse(resp.assertHeader('not a header', 'not a value'))

        self.assertFalse(resp.assertNotHeader('content-type'))
        self.assertFalse(resp.assertNotHeader('content-type', 'text/html'))
        self.assertTrue(resp.assertNotHeader('content-type', 'plain/text'))
        self.assertTrue(resp.assertNotHeader('not a header'))
        self.assertTrue(resp.assertNotHeader('not a header', 'not a value'))

    @patch("webunit2.utils.parse_cookies", Mock(return_value=None))
    def test_assert_cookie(self):
        """ Test that checking for cookies returns the correct values """
        resp = HttpResponse(self.mock_response)
