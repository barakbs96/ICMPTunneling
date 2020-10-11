"""Class ServerProxy."""
import socket
import random

from network.SecureICMPSocket import SecureICMPSocket
from network.ICMPSocket import ICMPSocket
from proxy.iproxy import IProxy
from tunnel.basic_tunnel import BasicTunnel
from config.proxy.httpproxy import (HTTP_PROXY_HOST, HTTP_PROXY_PORT,
                                    HTTP_PROXY_CLIENT_QUEUE)
from config.proxy.serverproxy import SERVER_PROXY_IP, SERVER_PROXY_PORT


class ServerProxy(IProxy):
    """Proxy from client to server."""

    def _create_listen_socket(self):
        """Create socket, bind and listen.

        Returns:
            Socket: Created socket.

        """
        listen_socket = socket.socket()
        listen_socket.bind((SERVER_PROXY_IP, SERVER_PROXY_PORT))
        listen_socket.listen(HTTP_PROXY_CLIENT_QUEUE)
        return listen_socket

    def start_proxy(self):
        """Start proxy server."""
        listen_socket = self._create_listen_socket()
        while True:
            client = listen_socket.accept()[0]
            server = SecureICMPSocket(HTTP_PROXY_HOST,
                                      random.randint(30000, 50000))
            server.connect()
            BasicTunnel(client, server).tunnel()
