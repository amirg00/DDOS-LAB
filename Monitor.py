from scapy.all import *
from scapy.layers.inet import IP, ICMP


def build_ping_packet(src_machine_ip, dst_machine_ip):
    ip = IP(src=src_machine_ip, dst=dst_machine_ip)
    icmp = ICMP()
    return ip / icmp


if __name__ == '__main__':
    args_list = sys.argv[1:]
    src_machine_ip, server_machine_ip = args_list

    while True:
        icmp_pkt = build_ping_packet(src_machine_ip, server_machine_ip)

        # Send the ping packet to server
        send(icmp_pkt)

        # Wait for 5 seconds
        time.sleep(5)
