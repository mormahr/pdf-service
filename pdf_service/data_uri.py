import re

from base64 import urlsafe_b64decode
from urllib.parse import unquote
from .errors import InvalidDataURI

# Adapted from https://github.com/fcurella/python-datauri

MIMETYPE_REGEX = r"[\w]+\/[\w\-\+\.]+"
_MIMETYPE_RE = re.compile("^{}$".format(MIMETYPE_REGEX))

CHARSET_REGEX = r"[\w\-\+\.]+"
_CHARSET_RE = re.compile("^{}$".format(CHARSET_REGEX))

DATA_URI_REGEX = (
        r"data:"
        + r"(?P<mimetype>{})?".format(MIMETYPE_REGEX)
        + r"(?:\;name\=(?P<name>[\w\.\-%!*'~\(\)]+))?"
        + r"(?:\;charset\=(?P<charset>{}))?".format(CHARSET_REGEX)
        + r"(?P<base64>\;base64)?"
        + r",(?P<data>.*)"
)
_DATA_URI_RE = re.compile(r"^{}$".format(DATA_URI_REGEX), re.DOTALL)


def parse(self):
    match = _DATA_URI_RE.match(self)
    if not match:
        raise InvalidDataURI("Not a valid data URI: %r" % self)
    mimetype = match.group("mimetype") or None
    name = match.group("name") or None
    charset = match.group("charset") or None

    if match.group("base64"):
        _charset = charset or "utf-8"
        _data = bytes(match.group("data"), _charset)
        data = urlsafe_b64decode(_data)
    else:
        data = unquote(match.group("data"))

    return mimetype, name, charset, bool(match.group("base64")), data
