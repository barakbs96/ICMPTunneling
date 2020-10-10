"""Class HTProxy."""
import threading
import socket

from proxy.iproxy import IProxy
from network.ICMPSocket import ICMPSocket
from tunnel.basic_tunnel import BasicTunnel
from config.proxy.httpproxy import (HTTP_PROXY_HOST, HTTP_PROXY_PORT,
                                    MAX_REQ_SIZE, HTTP_PROXY_CLIENT_QUEUE,
                                    HTTP_CONNECT_METHOD, HTTP_HOST_HEADER,
                                    HTTP_PROXY_CONNECT_MESSEGE)


class HTProxy(IProxy):
    """HTTP proxy over socket."""

    def _create_listen_socket(self):
        """Create socket, bind and listen.

        Returns:
            Socket: created socket.

        """
        listen_socket = socket.socket()
        listen_socket.bind((HTTP_PROXY_HOST, HTTP_PROXY_PORT))
        listen_socket.listen(HTTP_PROXY_CLIENT_QUEUE)
        return listen_socket

    def _get_host_data(self, request):
        """Extract host and port from client request.

        Args:
            request (String): Client request.

        Returns:
            Tuple: host and port.

        """
        host = ''
        port = 80
        for line in request.split('\n'):
            headers = [x.strip().lower() for x in line.split(':')]
            if headers[0] == HTTP_HOST_HEADER:
                host = headers[1]
                try:
                    port = int(headers[2])
                except Exception as e:
                    pass
                break
        return host, port

    def _serve_request(self, client):
        """Handle client request over proxy.

        Args:
            client (Socket): Client socket.
        """
        data = client.recv(MAX_REQ_SIZE)
        host, port = self._get_host_data(data)
        print host, port
        host_ip = socket.gethostbyname(host)
        tunnel_socket = socket.socket()
        tunnel_socket.connect((host_ip, port))
        if data.startswith(HTTP_CONNECT_METHOD):
            client.send(HTTP_PROXY_CONNECT_MESSEGE)
        else:
            tunnel_socket.send(data)
        BasicTunnel(client, tunnel_socket).tunnel()

    def start_proxy(self):
        """Start proxy server."""
        listen_socket = self._create_listen_socket()
        while True:
            request_socket = listen_socket.accept()[0]
            threading.Thread(target=self._serve_request,
                             args=(request_socket,)).start()
