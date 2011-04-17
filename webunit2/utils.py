import re
import urlparse


RE_PROTOCOL_SERVER = re.compile(r"^(http|https):\/\/\/*[\w\.\-]+")


def parse_url(url):
    """ Takes a URL string and returns its protocol and server """
    # Verify that the protocol makes sense.  We shouldn't guess!
    if not RE_PROTOCOL_SERVER.match(url):
        raise Exception("URL should begin with `protocol://domain`")

    protocol, server, path, _, _, _ = urlparse.urlparse(url)

    return protocol, server
