"""Class ServerProxy."""
import socket
import random

from network.secure_icmp_socket import SecureICMPSocket
from network.icmp_socket import ICMPSocket
from proxy.iproxy import IProxy
from tunnel.basic_tunnel import BasicTunnel
from config.proxy.http import (HTTP_PROXY_IP, HTTP_PROXY_PORT,
                               MAX_CLIENTS_HTTP_PROXY)
from config.proxy.server import SERVER_PROXY_IP, SERVER_PROXY_PORT


class ServerProxy(IProxy):
    """Proxy from client to server."""

    def _create_listen_socket(self):
        """Create socket, bind and listen.

        Returns:
            Socket: Created socket.

        """
        listen_socket = socket.socket()
        listen_socket.bind((SERVER_PROXY_IP, SERVER_PROXY_PORT))
        listen_socket.listen(MAX_CLIENTS_HTTP_PROXY)
        return listen_socket

    def start_proxy(self):
        """Start proxy server."""
        listen_socket = self._create_listen_socket()
        while True:
            client = listen_socket.accept()[0]
            server = SecureICMPSocket(HTTP_PROXY_IP,
                                      random.randint(30000, 50000))
            server.connect()
            BasicTunnel(client, server).tunnel()
