from proxy.ht_proxy import HTProxy
from network.SecureICMPSocket import SecureICMPSocket

class ICMPHTTPProxy(HTProxy):
    def _create_listen_socket(self):
        server_socket = SecureICMPSocket()
        server_socket.bind()
        return server_socket