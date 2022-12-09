import argparse
from scapy.all import *
from scapy.layers.inet import IP, ICMP


def build_ping_packet(src_machine_ip, dst_machine_ip):
    ip = IP(src=src_machine_ip, dst=dst_machine_ip)
    icmp = ICMP(type=8, code=0)
    return ip / icmp


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # Source ip: -s x.x.x.x
    parser.add_argument("-s", "--src", dest="src", help="source ip")
    # Destination ip: -d x.x.x.x
    parser.add_argument("-d", "--dest", dest="dest", help="destination ip")
    # -l python/c
    parser.add_argument("-l", "--lang", dest="language", help="current language")

    parser_args = parser.parse_args()
    print(parser_args.language == "python ")
    if parser_args.language.lower() != 'c' and parser_args.language.lower() != 'python':
        print("Bad input for flag language")
        exit(0)

    ping_results_file_name = "pings_results_c.txt" if parser_args.language.lower() == "c" else "pings_results_p.txt"
    ping_result_file = open(ping_results_file_name, "w")

    rtt_accumulator = 0
    pkt_cnt = 0

    src_machine_ip = parser_args.src
    server_machine_ip = parser_args.dest

    while True:
        try:
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
            pkt_cnt += 1

            # Wait for 5 seconds
            time.sleep(5)

        # User has terminated the program so right final bottom line
        except KeyboardInterrupt:
            break

    # Write bottom line: RTT average number
    write_final_line = f"{'-' * 100}\nAverage RTT (Round Trip Time): {rtt_accumulator / pkt_cnt}"
    ping_result_file.write(write_final_line)
    ping_result_file.close()
