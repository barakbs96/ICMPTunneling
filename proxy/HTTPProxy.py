import socket
import threading

from network.ICMPSocket import ICMPSocket
from proxy.IProxy import IProxy
from tunnel.Tunnel import Tunnel
from config.proxy.httpproxy import HTTP_PROXY_HOST, HTTP_PROXY_PORT, MAX_REQ_SIZE, HTTP_PROXY_CLIENT_QUEUE,\
    HTTP_CONNECT_METHOD, HTTP_HOST_HEADER, HTTP_PROXY_CONNECT_MESSEGE

class HTTPProxy(IProxy):
    def setup_client(self, data):
        host = ''
        port = 80
        for line in data.split('\n'):
            headers = [x.strip().lower() for x in line.split(':')]
            if headers[0] == HTTP_HOST_HEADER:
                host = headers[1]
            try:
                port = int(headers[2])
            except Exception as e:
                pass
        return host, port

    def handle_client(self, client):
        data = client.recv(MAX_REQ_SIZE)
        host, port = self.setup_client(data)
        print host, port
        proxy_socket = socket.socket()
        proxy_socket.connect((socket.gethostbyname(host), port))
        if data.startswith(HTTP_CONNECT_METHOD):
            client.send(HTTP_PROXY_CONNECT_MESSEGE)
        else:
            proxy_socket.send(data)
        tunnel = Tunnel(client, proxy_socket)
        tunnel.start_tunneling()

    def _setup_server_socket(self):
        server_socket = socket.socket()
        server_socket.bind((HTTP_PROXY_HOST, HTTP_PROXY_PORT))
        server_socket.listen(HTTP_PROXY_CLIENT_QUEUE)
        return server_socket

    def serve(self):
        server_socket = self._setup_server_socket()
        while True:
            client_socket = server_socket.accept()[0]
            handle_client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            handle_client_thread.start()
