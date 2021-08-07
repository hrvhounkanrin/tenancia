import os
import re
import sys


def read_env():
    """This functions aim to reads local default
    environment variables from a .env file located in the project root
    directory.
    """
    try:
        with open(".env") as f:
            content = f.read()
    except OSError:
        content = ""

    for line in content.splitlines():
        m1 = re.match(r"\A([A-Za-z_0-9]+)=(.*)\Z", line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r"\\(.)", r"\1", m3.group(1))
            os.environ.setdefault(key, val)


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
