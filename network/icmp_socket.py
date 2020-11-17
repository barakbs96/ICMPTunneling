"""Class ICMPSocket."""
from scapy.all import *

from network.isocket import ISocket
from config.network.icmp import (CODE_MESSAGE_CONNECT, INDEX_PORT, BPF_CONNECT,
                                 BPF_DATA, CODE_MESSAGE_ICMP_DATA,
                                 BPF_CONNECT_ACK, CODE_MESSAGE_CONNECT_ACK,
                                 CLIENT_MAGIC, SERVER_MAGIC, TIMEOUT_SNIFF,
                                 CODE_MESSAGE_DATA_CHUNK,
                                 CODE_MESSAGE_DATA_CHUNK_END, MESSAGE_MAX_SIZE,
                                 CHUNK_END_MAGIC)


class ICMPSocket(ISocket):
    """Socket object using icmp packets."""

    def __init__(self, ip='', port=0):
        """Initialize socket ip and port.

        Args:
            ip (str, optional): IP address which the socket will connect to or
            listen on.
            port (int, optional): Port number which the socket will connect to
            or listen on.
        """
        self._ip = ip
        self._port = port
        self._data_buffer = []
        self._id = CLIENT_MAGIC
        self._response_id = SERVER_MAGIC

    def _receive_packets(self, buffer):
        """
        Receive packets by sniffing on icmp data type filter.

        Sniffing for packets matches the response id and the wanted port.

        Args:
            buffer (array): Array bufffer which every packet data and type will
            be saved to as a tuple.
        """
        while True:
            try:
                sniff(filter=BPF_DATA,
                      lfilter=lambda x: (x[ICMP].type == self._response_id and
                                         x[ICMP].seq == self._port),
                      prn=lambda x: buffer.append((x[ICMP].load, x[ICMP].code))
                      )
            except Exception as e:
                pass

    def connect(self):
        """Will send icmp connect packet and snif for icmp ack message."""
        connect_packet = IP(dst=self._ip) / ICMP(code=CODE_MESSAGE_CONNECT,
                                                 seq=self._port,
                                                 type=self._id)
        send(connect_packet, verbose=False)
        try:
            sniff(filter=BPF_CONNECT_ACK, lfilter=lambda x: (
                x[ICMP].seq == self._port and
                x[ICMP].type == self._response_id),
                count=1,
                timeout=TIMEOUT_SNIFF)[0]
        except Exception as e:
            pass

        threading.Thread(target=self._receive_packets,
                         args=(self._data_buffer,)).start()

    def bind(self):
        """Bind the socket to address."""
        pass

    def _set_as_server(self):
        """Start serving as server and receive packets."""
        self._id = SERVER_MAGIC
        self._response_id = CLIENT_MAGIC
        threading.Thread(target=self._receive_packets,
                         args=(self._data_buffer,)).start()

    def accept(self):
        """
        Wait for icmp connect packet.

        when one arrived, create a connection using ICMPSocket.

        Returns:
            connection tuple: tuple contains client socket and client details.

        """
        icmp_packet = sniff(filter=BPF_CONNECT, count=1)[0]
        src_ip = icmp_packet[IP].src
        src_port = icmp_packet[ICMP].fields[INDEX_PORT]
        client_socket = self.__class__(src_ip, src_port)
        client_socket._set_as_server()
        connect_ack_packet = IP(dst=src_ip) / ICMP(
                                                code=CODE_MESSAGE_CONNECT_ACK,
                                                seq=src_port, type=SERVER_MAGIC
                                                )
        send(connect_ack_packet, verbose=False)
        return (client_socket, (src_ip, src_port))

    def send(self, data):
        """
        Send data over icmp packets.

        Fragment data if needed.

        Args:
            data (string): Data to send.

        Returns:

        """
        if len(data) <= MESSAGE_MAX_SIZE:
            data_icmp_packet = IP(dst=self._ip) / ICMP(
                                                code=CODE_MESSAGE_ICMP_DATA,
                                                seq=self._port,
                                                type=self._id) / data
            send(data_icmp_packet, verbose=False)
            return
        for i in xrange(len(data) / MESSAGE_MAX_SIZE + 1):
            data_chunk = data[MESSAGE_MAX_SIZE * i: MESSAGE_MAX_SIZE * (i + 1)]
            chunk_icmp_packet = IP(dst=self._ip) / ICMP(
                                                code=CODE_MESSAGE_DATA_CHUNK,
                                                seq=self._port,
                                                type=self._id) / data_chunk
            send(chunk_icmp_packet, verbose=False)
        chunk_end_icmp_packet = IP(dst=self._ip) / ICMP(
                                            code=CODE_MESSAGE_DATA_CHUNK_END,
                                            seq=self._port,
                                            type=self._id) / CHUNK_END_MAGIC
        send(chunk_end_icmp_packet, verbose=False)

    def recv(self, bufsize=0):
        """
        Receive data over icmp packets.

        Args:
            bufsize (int): The maximum amount of data to be received at once.

        Returns:
            string: Data received.

        """
        while len(self._data_buffer) == 0:
            pass
        icmp_data = self._data_buffer.pop()
        if icmp_data[1] == CODE_MESSAGE_ICMP_DATA:
            return icmp_data[0]
        elif icmp_data[1] == CODE_MESSAGE_DATA_CHUNK:
            data = ''
            while icmp_data[1] != CODE_MESSAGE_DATA_CHUNK_END:
                data += icmp_data[0]
                while len(self._data_buffer) == 0:
                    pass
                icmp_data = self._data_buffer.pop()
            return data
