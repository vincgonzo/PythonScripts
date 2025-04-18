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

class C2Commands(Enum):
    CLS = "client"
    CLS_DWN = "client download"
    CLS_UP = "client upload"
    CLS_ZIP = "client zip"
    CLS_UZIP = "client unzip"
    CLS_SLP = "client sleep "
    CLS_KLL = "client kill"
    SERV = "server"
    SERV_EXT = "server exit"
    SERV_ZIP = "server zip"
    SERV_UZIP = "server unzip"
    SERV_CTRL = "server control "
    SERV_SH_CLS = "server show clients"
    CD = "cd "

PORT = 8900


# Leave blank to bind to all int otherwise specify c2 server IP address
BIND_ADDR = ""

PROXY = None

C2_SERVER = "localhost"
FILE_SEND = "/reviews"
CMD_REQUEST = "/student?isbn="
FILE_REQUEST = "/author?name="
RESPONSE_PATH = "/library"
CWD_RESPONSE = "/title"
RESPONSE_KEY = "index"

INCOMING = "incoming"
OUTGOING = "outgoing"

HEADER: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

INPUT_TIMEOUT = 225
#INPUT_TIMEOUT = None

# Run this cmd automatically to prevent Azure and other hosting env from killing our active session.
if platform.system() == "Windows":
    KEEP_ALIVE_CMD = "time /T" # windows only
else:
    KEEP_ALIVE_CMD = "date +%R" # linux only

DELAY = 3

ZIP_PASSWORD = b"*--->C2_FOR_LIFE<---*"

# <=32 character
KEY = "myHughSecretKey"
KEY_LEN_REQ = 32