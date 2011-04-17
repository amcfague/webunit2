import unittest
from webunit2.utils import parse_cookies, parse_url

class TestUtilities(unittest.TestCase):

    def test_parse_url_valid_url(self):
        """ Test that a valid URL is parsed into a protocol and server """
        test_urls = {
            "http://test.com":      ("http", "test.com"),
            "http://test.com:80":   ("http", "test.com:80"),
            "https://test.com":     ("https", "test.com"),
            "https://test.com:443": ("https", "test.com:443")
        }

        for url, parts in test_urls.items():
            self.assertEqual(parse_url(url), parts)

    def test_parse_url_invalud_url(self):
        """ Test that an Exception is thrown on an invalid URL """
        self.assertRaises(Exception, parse_url, "bad_url")
        self.assertRaises(Exception, parse_url, "https://")
        self.assertRaises(Exception, parse_url, "gopher://")

    def test_parse_cookies(self):
        cookie_str = "name1=val1; EXPIres=Wed, 09 Jun 2021 10:18:14 GMT; HttpOnLy"
        cookies = parse_cookies(cookie_str)
        expected_cookies = {
            "name1": {
                "name1": "val1",
                "expires": "Wed, 09 Jun 2021 10:18:14 GMT",
                "httponly": True,
                "secure": False,
            }
        }

        self.assertEqual(cookies, expected_cookies)
