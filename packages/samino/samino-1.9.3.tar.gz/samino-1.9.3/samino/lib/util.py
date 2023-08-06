from base64 import b64encode, b64decode
from hashlib import sha1
from uuid import uuid4
import platform
import logging
import socket
import uuid
import json
import hmac
import re

api = "https://service.narvii.com/api/v1{}".format
tapjoy = "https://ads.tapdaq.com/v4/analytics/reward"


def sh(key: str, data: bytes):
    return hmac.new(bytes.fromhex(b64decode(key).decode()[::-1]), data, sha1)


def get_unique_id():
    try:
        info = {
            "platform": platform.system(),
            "platform-release": platform.release(),
            "platform-version": platform.version(),
            "architecture": platform.machine(),
            "hostname": socket.gethostname(),
            "ip-address": socket.gethostbyname(socket.gethostname()),
            "mac-address": ":".join(re.findall("..", "%012x" % uuid.getnode())),
            "processor": platform.processor(),
        }
        return b64encode(sh("ZTNkYmYxNzkxOGE1MzRiNzdlMWI4YjczMWVkYWNjYWE2NTFhNGI2Nw==", json.dumps(info).encode()).digest())
    except Exception as e:
        logging.exception(e)


def c(value: bytes = get_unique_id()):
    return (
        b64decode("MzI=").decode() +
        value.hex() +
        sh("ZTNkYmYxNzkxOGE1MzRiNzdlMWI4YjczMWVkYWNjYWE2NTFhNGI2Nw==", b64decode(b"Mg==") + value).hexdigest()
    ).upper()


def s(data):
    return b64encode(
        b64decode(b"Mg==") +
        sh("MmU0ZDk2YTY4MjNmOWVjMDFiMzk1NWVlMjQwOWE3MGEzYmU4OWZiZg==", data.encode()).digest()
    ).decode()


def uu():
    return str(uuid4())
