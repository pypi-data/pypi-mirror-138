import socket

from scapy.layers.inet import TCP, IP
from scapy.packet import Raw
from scapy.utils import rdpcap

from .zoomzoom import run_in_another_thread


@run_in_another_thread
def play_capture(capture_file):
    """
    Plays a capture file back using the first packet's destination address
    :param capture_file:
    :return:
    """
    print(capture_file)
    pkts = rdpcap(capture_file)
    with socket.socket(socket.AF_INET) as s:
        s.connect((pkts[0][IP].dst, pkts[0][TCP].dport))
        for pkt in pkts:
            if pkt.haslayer(Raw):
                s.send(bytes(pkt[Raw]))


def test_func(cap_name):
    play_capture(cap_name)


if __name__ == '__main__':
    test_func('sample.pcapng')
