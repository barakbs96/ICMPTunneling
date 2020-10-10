import socket
import random

from network.SecureICMPSocket import SecureICMPSocket
from network.ICMPSocket import ICMPSocket
from proxy.iproxy import IProxy
from tunnel.basic_tunnel import BasicTunnel
from config.proxy.httpproxy import HTTP_PROXY_HOST, HTTP_PROXY_PORT, HTTP_PROXY_CLIENT_QUEUE
from config.proxy.serverproxy import SERVER_PROXY_IP, SERVER_PROXY_PORT

class ServerProxy(IProxy):
    def _create_listen_socket(self):
        server_socket = socket.socket()
        server_socket.bind((SERVER_PROXY_IP, SERVER_PROXY_PORT))
        server_socket.listen(HTTP_PROXY_CLIENT_QUEUE)
        return server_socket

    def start_proxy(self):
        server_socket = self._create_listen_socket()
        while True:
            client = server_socket.accept()[0]
            random_port = random.randint(30000, 50000)
            server = SecureICMPSocket(HTTP_PROXY_HOST, random_port)
            server.connect()
            tunnel = BasicTunnel(client, server)
            tunnel.tunnel()
