"""ICMP consts.

Attributes:
    BPF_CONNECT (TYPE): BFF filter for connect message sniffing.
    BPF_CONNECT_ACK (TYPE): BFF filter for conncect ack message sniffing.
    BPF_DATA (TYPE): BFF filte for data icmp packet sniffing.
    CHUNK_END_MAGIC (str): String represents end of data chunks.
    CLIENT_MAGIC (int): String identifies client.
    CODE_MESSAGE_CONNECT (int): code message for connect method.
    CODE_MESSAGE_CONNECT_ACK (int): code message for connect ack method.
    CODE_MESSAGE_DATA_CHUNK (int): code message for data chunk method.
    CODE_MESSAGE_DATA_CHUNK_END (int): code message for chunk end method.
    CODE_MESSAGE_ICMP_DATA (int): code message for data method.
    INDEX_PORT (str): Index of port in icmp packet.
    MESSAGE_MAX_SIZE (int): Max size of data in icmp packet.
    SERVER_MAGIC (int): String represents server.
    TIMEOUT_SNIFF (int): Timeout for sniffing one packet.

"""
CLIENT_MAGIC = 8
SERVER_MAGIC = 0

TIMEOUT_SNIFF = 15
MESSAGE_MAX_SIZE = 1024

INDEX_PORT = 'seq'
CODE_MESSAGE_CONNECT = 100
CODE_MESSAGE_CONNECT_ACK = 101
CODE_MESSAGE_ICMP_DATA = 102
CODE_MESSAGE_DATA_CHUNK = 103
CODE_MESSAGE_DATA_CHUNK_END = 104
CHUNK_END_MAGIC = 'xxxx'

BPF_CONNECT = 'icmp[icmpcode]=={0}'.format(str(CODE_MESSAGE_CONNECT))
BPF_CONNECT_ACK = 'icmp[icmpcode]=={0}'.format(str(CODE_MESSAGE_CONNECT_ACK))
BPF_DATA = 'icmp[icmpcode]=={0} or icmp[icmpcode]=={1} or icmp[icmpcode]=={2}'\
    .format(str(CODE_MESSAGE_ICMP_DATA),
            str(CODE_MESSAGE_DATA_CHUNK),
            str(CODE_MESSAGE_DATA_CHUNK_END))
