from matplotlib import pyplot as plt

title = 'RTT For Ping Packets'
x_label = 'RTT (milliseconds)'
y_label = 'RTT (milliseconds)'


x = [i for i in range(1000000)]
y = [i*i for i in range(1000000)]


def get_syn_pkts_graph():
    pass


def get_pings_pkts_graph():
    pass


if __name__ == '__main__':
    plt.semilogx(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
