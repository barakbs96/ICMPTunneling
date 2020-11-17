"""Class HTProxy."""
import threading
import socket

from proxy.iproxy import IProxy
from network.icmp_socket import ICMPSocket
from tunnel.basic_tunnel import BasicTunnel
from config.proxy.http import (HTTP_PROXY_IP, HTTP_PROXY_PORT,
                               MAX_DATA_SIZE, MAX_CLIENTS_HTTP_PROXY,
                               CONNECT_HTTP_METHOD, HOST_HTTP_HEADER,
                               PROXY_CONNECT_HTTP_MESSEGE)


class HTProxy(IProxy):
    """HTTP proxy over socket."""

    def _create_listen_socket(self):
        """Create socket, bind and listen.

        Returns:
            Socket: created socket.

        """
        listen_socket = socket.socket()
        listen_socket.bind((HTTP_PROXY_IP, HTTP_PROXY_PORT))
        listen_socket.listen(MAX_CLIENTS_HTTP_PROXY)
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
            if headers[0] == HOST_HTTP_HEADER:
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
        data = client.recv(MAX_DATA_SIZE)
        host, port = self._get_host_data(data)
        print host, port
        host_ip = socket.gethostbyname(host)
        tunnel_socket = socket.socket()
        tunnel_socket.connect((host_ip, port))
        if data.startswith(CONNECT_HTTP_METHOD):
            client.send(PROXY_CONNECT_HTTP_MESSEGE)
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
