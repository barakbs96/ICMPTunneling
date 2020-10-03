import socket
import random

from network.SecureICMPSocket import SecureICMPSocket
from network.ICMPSocket import ICMPSocket
from proxy.IProxy import IProxy
from tunnel.Tunnel import Tunnel
from config.proxy.httpproxy import HTTP_PROXY_HOST, HTTP_PROXY_PORT, HTTP_PROXY_CLIENT_QUEUE
from config.proxy.serverproxy import SERVER_PROXY_IP, SERVER_PROXY_PORT

class ServerProxy(IProxy):
    def _setup_server_socket(self):
        server_socket = socket.socket()
        server_socket.bind((SERVER_PROXY_IP, SERVER_PROXY_PORT))
        server_socket.listen(HTTP_PROXY_CLIENT_QUEUE)
        return server_socket

    def serve(self):
        server_socket = self._setup_server_socket()
        while True:
            client = server_socket.accept()[0]
            random_port = random.randint(30000, 50000)
            server = SecureICMPSocket(HTTP_PROXY_HOST, random_port)
            server.connect()
            tunnel = Tunnel(client, server)
            tunnel.start_tunneling()
