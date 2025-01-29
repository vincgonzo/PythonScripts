#!/bin/python3

import sys
import socket 
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def usage():
    print("""
    Netcat Python 3 Tool
    Usage: netcat.py -t <target_host> -p <port>
    -l --listen             - listen on [host]:[port] for incoming connection
    -e --exec=file_to_run   - execute the given file upon receiving a connection
    -c --command            - initialize a command shell
    -u --upload=destination - upon receiving connection upload a file and write to [destination]

    Examples: 
    netcat.py -t 192.168.0.1 -p 5555 -l -c
    netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe
    netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"
    echo 'ABCDEFG' | ./netcat.py -t 192.168.11.12 -p 135
    """)
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
   
    if not len(sys.argv[1:]):
        usage()
    #read cmdlines
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:",["help","listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"

    if not listen and len(target) and port > 0:
        #read in the buf from cmdline if block enter CTRL+D
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()


def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer.encode('utf-8'))
        
        while True:
            # wait for datas to comme
            recv_len = 1
            response = b''

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                if recv_len < 4096:
                    break

            
            print(response.decode('utf-8'), end=' ')

            # wait for more input
            buffer = input("")
            buffer += "\n"
            # send it
            client.send(buffer.encode('utf-8'))

    
    except socket.error as exc:
        # just catch generic errors - you can do your homework to beef this up
        print("[*] Exception! Exiting.")
        print(f"[*] Caught exception socket.error: {exc}")

        # teardown the connection
        client.close()

def server_loop():
    global target
    
    # if no traget define we listenn all interfaces
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    print(f"[*] Listening on {target}:{port}...")
    try:
        while True:
            client_socket, addr = server.accept()
            print(f"[*] Connection received from {addr[0]}:{addr[1]}")

            client_thread = threading.Thread(target=client_handler, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\n[*] Exiting server loop...")
        server.close()
        sys.exit(0)    

    
def run_command(command):
    # trim new line
    command = command.rstrip()

    # run cmd & get output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to exec cmd.\r\n"
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):

        # read in all of the bytes and write to our destination
        file_buffer = ""

        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        # now we take these bytes and try to write them out
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer.encode('utf-8'))
            file_descriptor.close()

            # acknowledge that we wrote the file out
            client_socket.send(
                "Successfully saved file to %s\r\n" % upload_destination)
        except OSError:
            client_socket.send(
                "Failed to save file to %s\r\n" % upload_destination)

    # check for command execution
    if len(execute):
        # run the command
        output = run_command(execute)

        client_socket.send(output)

    # now we go into another loop if a command shell was requested
    if command:

        while True:
            # show a simple prompt
            client_socket.send("<VcgZ0:#> ".encode('utf-8'))

            # now we receive until we see a linefeed (enter key)
            cmd_buffer = b''
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # we have a valid command so execute it and send back the results
            response = run_command(cmd_buffer.decode())

            # send back the response
            client_socket.send(response)


main()
