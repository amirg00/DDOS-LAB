import argparse

from matplotlib import pyplot as plt


def get_syns_packets_num(file_lines):
    return int((len(file_lines) - 2) / 2)


def get_pings_packets_num(file_lines):
    return int(len(file_lines) - 2)


def get_syn_pkts_graph(file_name):
    title = 'Packet Sending Time'
    y_label = 'Sending Time (seconds)'
    x_label = 'Packet NO.'
    y = []

    file = open(file_name, "r")
    file_lines = file.readlines()
    print(get_syns_packets_num(file_lines))
    x = [i for i in range(get_syns_packets_num(file_lines))]

    for line in file_lines:
        if "time taken" in line:
            send_time = line[33:-10]
            print(send_time)
            y.append(float(send_time))

    print(x, y)
    set_plt_vars(title, x_label, y_label, x, y)


def get_pings_pkts_graph(file_name):
    title = 'RTT For Ping Packets'
    y_label = 'RTT (milliseconds)'
    x_label = 'Packet NO.'
    y = []

    file = open(file_name, "r")
    file_lines = file.readlines()
    print(get_pings_packets_num(file_lines))
    x = [i for i in range(get_pings_packets_num(file_lines))]

    for line in file_lines:
        if "time taken" in line:
            send_time = line[61:-10]
            print(send_time)
            y.append(1000 * float(send_time))

    print(x, y)
    set_plt_vars(title, x_label, y_label, x, y)


def set_plt_vars(title, x_label, y_label, x, y):
    plt.semilogx(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # -f file_name.txt
    parser.add_argument("-f", "--file_name", dest="file_name", help="file name")

    parser_args = parser.parse_args()

    if parser_args.file_name == "syns_results_c.txt":
        get_syn_pkts_graph("syns_results_c.txt")

    elif parser_args.file_name == "syns_results_p.txt":
        get_syn_pkts_graph("syns_results_p.txt")

    elif parser_args.file_name == "pings_results_c.txt":
        get_pings_pkts_graph("pings_results_c.txt")

    elif parser_args.file_name == "pings_results_p.txt":
        get_pings_pkts_graph("pings_results_p.txt")

    else:
        print("Error: file isn't compatible to any of the lab's files.")
