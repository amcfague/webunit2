import re
import urlparse
import logging


RE_PROTOCOL_SERVER = re.compile(r"^(http|https):\/\/\/*[\w\.\-]+")
RE_COOKIE_STRINGS = re.compile(r"(?<!expires=...), ", re.IGNORECASE)

log = logging.getLogger(__name__)

def parse_cookies(set_cookie_headers):
    if not set_cookie_headers:
        return {}

    # httplib2 joins all the cookies by commas... break them apart here!
    # Unfortunately, commas are also used in dates, so be clever here.
    # TODO How reliable is this?
    all_cookie_strings = RE_COOKIE_STRINGS.split(set_cookie_headers)

    cookies = {}
    for cookie_str in all_cookie_strings:
        cookie_attr_strs = re.split(r'; +', cookie_str)

        # The first entry in a cookie is ALWAYS `name=value`
        cookie_name, cookie_value = tuple(cookie_attr_strs[0].split("=", 1))

        cookie_attr_dict = {"secure": False, "httponly": False}
        for part in cookie_attr_strs:
            part_lower = part.lower()
            if part_lower in ["secure", "httponly"]:
                cookie_attr_dict[part_lower] = True
            elif "=" in part:
                key, value = part.split("=", 1)
                cookie_attr_dict[key.lower()] = value
            else:
                log.error("Unknown cookie detected: %s", part)
                raise CookieException("Invalid cookie: %s" % cookie_str)


        cookies[cookie_name.lower()] = cookie_attr_dict

    return cookies


def parse_url(url):
    """ Takes a URL string and returns its protocol and server """
    # Verify that the protocol makes sense.  We shouldn't guess!
    if not RE_PROTOCOL_SERVER.match(url):
        raise Exception("URL should begin with `protocol://domain`")

    protocol, server, path, _, _, _ = urlparse.urlparse(url)

    return protocol, server

class CookieException(Exception):
    pass