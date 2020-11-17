"""Class ISocket."""


class ISocket(object):
    """Interface for a socket object."""

    def connect(self):
        """Connect to a remote socket at address.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError

    def bind(self):
        """Bind the socket to address.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError

    def accept(self):
        """Accept a connection.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError

    def recv(self, bufsize):
        """Receive data from the socket.

        Args:
            bufsize (int): The maximum amount of data to be received at once.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError

    def send(self, data):
        """Send data to the socket.

        Args:
            data (string): Data to send.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError
