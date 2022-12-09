import argparse
from scapy.all import *
from scapy.layers.inet import IP, ICMP


def build_ping_packet(src_machine_ip, dst_machine_ip):
    ip = IP(src=src_machine_ip, dst=dst_machine_ip)
    icmp = ICMP()
    return ip / icmp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # -l python/c
    parser.add_argument("-l", "--lang", dest="language", help="current language")

    parser_args = parser.parse_args()
    if parser_args.language.lower() != 'c' or parser_args.language.lower() != 'python':
        print("Bad input for flag language")
        exit(0)

    ping_results_file_name = "pings_results_c.txt" if parser_args.language.lower() == "c" else "pings_results_p.txt"
    ping_result_file = open(ping_results_file_name, "w")

    rtt_accumulator = 0
    pkt_cnt = 0

    args_list = sys.argv[1:]
    src_machine_ip, server_machine_ip = args_list

    while True:
        icmp_pkt = build_ping_packet(src_machine_ip, server_machine_ip)

        # Save current time before sending
        start = time.time()

        # Send and receive the ping packet to server
        sr1(icmp_pkt)

        # Save current time after receiving
        finish = time.time()

        # Calculate the round trip time of the packet.
        RTT = finish - start
        rtt_accumulator += RTT

        # Write result to file and save it in an accumulator variable for total average
        write_str = f"Total time taken to send and receive ping packet NO.{pkt_cnt} (RTT): {RTT} seconds.\n"
        ping_result_file.write(write_str)

        # Wait for 5 seconds
        time.sleep(5)

    write_final_line = f"{'-' * 70}\nAverage RTT (Round Trip Time): {rtt_accumulator / pkt_cnt}"
    file.write(write_final_line)
    file.close()
