"""Class IProxy."""


class IProxy(object):
    """Interface for a proxy object."""

    def _create_listen_socket(self):
        """
        Create and listen on a socket.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError

    def start_proxy(self):
        """
        Start serving as a Proxy.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError
