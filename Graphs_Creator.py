import argparse
import pandas as pd

import numpy as np
from matplotlib import pyplot as plt


def get_syns_packets_num(file_lines):
    return int((len(file_lines) - 2) / 2)


def get_pings_packets_num(file_lines):
    return int(len(file_lines) - 2)


def get_syn_pkts_graph(file_name):
    title = 'Packet Sending Time'
    x_label = 'Sending Time (seconds)'
    y_label = 'Packet NO.'
    send_time_lst = []

    file = open(file_name, "r")
    file_lines = file.readlines()
    print(get_syns_packets_num(file_lines))

    for line in file_lines:
        if "time taken" in line:
            send_time = line[33:-10]
            send_time_lst.append(float(send_time))

    sorted(send_time_lst)
    print(len(send_time_lst))

    # Convert the array to a pandas Series
    series = pd.Series(send_time_lst)

    # Create the intervals
    intervals = pd.cut(series, 5)

    # Count the number of times in each interval
    counts = intervals.value_counts().sort_index()

    # Calculate the middle of the intervals
    middle = [(interval.left + interval.right) / 2 for interval in intervals.cat.categories]

    # Set the labels for each interval
    labels = [f"{m:.5f}" for m in middle]

    # Calculate the positions for the bars
    positions = np.logspace(-7, -6, len(counts), base=10)

    # Set the width of the bars to be equal to the distance between the positions
    width = (positions[1] - positions[0]) * 0.5

    # Create the bar plot
    plt.bar(positions, counts, width=width)

    # Set the x-axis to a logarithmic scale
    plt.gca().set_xscale("log")
    plt.gca().set_yscale("log")

    # Set the labels for the x-axis
    plt.xticks(positions, labels)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    # Show the plot
    plt.show()


def get_pings_pkts_graph(file_name):
    title = 'RTT For Ping Packets'
    x_label = 'RTT (milliseconds)'
    y_label = 'Packet NO.'
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
