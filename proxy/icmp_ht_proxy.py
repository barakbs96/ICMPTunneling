"""Class ICMPHTProxy."""
from proxy.ht_proxy import HTProxy
from network.secure_icmp_socket import SecureICMPSocket


class ICMPHTProxy(HTProxy):
    """HTTP proxy over ICMP Socket."""

    def _create_listen_socket(self):
        """
        Create ICMP socket, bind and listen.

        Returns:
            Socket: Created ICMP socket.

        """
        listen_socket = SecureICMPSocket()
        listen_socket.bind()
        return listen_socket
