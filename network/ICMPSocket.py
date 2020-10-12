"""Summary
"""
from scapy.all import *

from network.ISocket import ISocket
from config.network.icmp import ICMP_CONNECT_MESSEGE_CODE, ICMP_PORT_FIELD, ICMP_CONNECT_FILTER, ICMP_DATA_FILTER,\
    ICMP_DATA_MESSEGE_CODE, ICMP_CONNECT_ACK_FILTER, ICMP_CONNECT_ACK_MESSEGE_CODE, ICMP_CLIENT_ID, ICMP_SERVER_ID,\
    ICMP_SOCKET_SNIFF_TIMEOUT, ICMP_FRAGMENTED_DATA_MESSEGE_CODE, ICMP_FRAGMENTED_DATA_DONE_MESSEGE_CODE,\
    MAX_ICMP_MESSAGE_SIZE


class ICMPSocket(ISocket):

    """Summary
    ICMP socket. 

    """
    
    def __init__(self, ip='', port=0):
        """Summary
        
        Args:
            ip (str, optional): Server's IP 
            port (int, optional): Server's connect port 
        """
        self._ip = ip
        self._port = port
        self._id = ICMP_CLIENT_ID
        self._response_id = ICMP_SERVER_ID
        self._buffer = []

    def _set_as_server(self):
        """Summary
        start Server. Listens for outgoing/incoming ICMP packets.
        """
        self._id = ICMP_SERVER_ID
        self._response_id = ICMP_CLIENT_ID
        t = threading.Thread(target=self._recv_packets, args=(self._buffer,))
        t.start()

    def bind(self):
        """Summary
        """
        pass

    def accept(self):
        """Summary
        
        Returns:
            tuple (client_socket, (ip,port)): Return tuple containg client socket and ip, port information. 
        """
        icmp_packet = sniff(filter=ICMP_CONNECT_FILTER, count=1)[0]
        ip = icmp_packet[IP].src
        port = icmp_packet[ICMP].fields[ICMP_PORT_FIELD]
        client_socket = self.__class__(ip, port)
        client_socket._set_as_server()
        icmp_connect_ack_packet = IP(dst=ip) / ICMP(code=ICMP_CONNECT_ACK_MESSEGE_CODE, seq=port, type=ICMP_SERVER_ID)
        send(icmp_connect_ack_packet, verbose=False)
        return (client_socket, (ip, port))

    def connect(self):
        """Summary
        
        """
        icmp_connect_packet = IP(dst=self._ip)/ICMP(code=ICMP_CONNECT_MESSEGE_CODE, seq=self._port, type=self._id)
        send(icmp_connect_packet, verbose=False)
        try:
            sniff(filter=ICMP_CONNECT_ACK_FILTER, lfilter=lambda x: x[ICMP].seq == self._port and x[ICMP].type == self._response_id, count=1, timeout=ICMP_SOCKET_SNIFF_TIMEOUT)[0]
        except Exception as e:
            pass
        t = threading.Thread(target=self._recv_packets, args=(self._buffer,))
        t.start()

    def _recv_packets(self, buffer):
        """Summary
        Listen for icmp packets. received ICMP packets are stroed into buffer.
        Args:
            buffer (TYPE): Write received ICMP packets to buffer.
        """
        while True:
            try:
                sniff(filter=ICMP_DATA_FILTER,
                      lfilter=lambda x: x[ICMP].seq == self._port and x[ICMP].type == self._response_id, prn=lambda x:buffer.append((x[ICMP].load, x[ICMP].code)))
            except Exception as e:
                pass


    def recv(self, amount=0):
        """Summary
        Read Received ICMP packets from buffer. extract from ICMP packet 
        Args:
            amount (int, optional): Description
        
        Returns:
            data: return the extracted data from ICMP packet. 
        """
        while len(self._buffer) == 0:
            pass
        icmp_data = self._buffer.pop()
        if icmp_data[1] == ICMP_DATA_MESSEGE_CODE:
            return icmp_data[0]
        elif icmp_data[1] == ICMP_FRAGMENTED_DATA_MESSEGE_CODE:
            data = ''
            while icmp_data[1] != ICMP_FRAGMENTED_DATA_DONE_MESSEGE_CODE:
                data += icmp_data[0]
                while len(self._buffer) == 0:
                    pass
                icmp_data = self._buffer.pop()
            return data

    def send(self, data):
        """Summary 
        Encapsolate IP traffic in ICMP echo packets and send them to our own proxy server. 
        Args:
            data (TYPE): Description
        
        Returns:
            TYPE: Description
        """
        # no need for fregmentation. data size is less then MAX_ICMP_MESSAGE_SIZE
        if len(data) <= MAX_ICMP_MESSAGE_SIZE:
            icmp_packet = IP(dst=self._ip)/ICMP(code=ICMP_DATA_MESSEGE_CODE, seq=self._port, type=self._id)/data
            send(icmp_packet, verbose=False)
            return
        # fregmentation packet
        for i in xrange(len(data)/MAX_ICMP_MESSAGE_SIZE+1):
            data_part = data[MAX_ICMP_MESSAGE_SIZE*i:MAX_ICMP_MESSAGE_SIZE*(i+1)]
            icmp_packet = IP(dst=self._ip) / ICMP(code=ICMP_FRAGMENTED_DATA_MESSEGE_CODE, seq=self._port, type=self._id)/data_part
            send(icmp_packet, verbose=False)
        # send done fregment message code type
        icmp_packet = IP(dst=self._ip) / ICMP(code=ICMP_FRAGMENTED_DATA_DONE_MESSEGE_CODE, seq=self._port,
                                              type=self._id) / 'abcd'
        send(icmp_packet, verbose=False)
