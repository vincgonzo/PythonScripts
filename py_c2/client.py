#!/bin/python3

from requests import get

PORT=8900

HEADER: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# PROXY = {"https": "proxy.some-site.com:443"}
PROXY = None

x = get(f'http://localhost:{PORT}', headers=HEADER, proxies=PROXY)

print(f"Response Object: {x.request.headers}\n\tHeader: {x.headers}\n\tReason: {x.reason}\n\tStatus: {x.status_code}")

