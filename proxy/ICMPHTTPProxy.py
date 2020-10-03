from proxy.HTTPProxy import HTTPProxy
from network.SecureICMPSocket import SecureICMPSocket

class ICMPHTTPProxy(HTTPProxy):
    def _setup_server_socket(self):
        server_socket = SecureICMPSocket()
        server_socket.bind()
        return server_socket