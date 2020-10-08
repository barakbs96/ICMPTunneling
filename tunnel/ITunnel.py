"""Class ITunnel."""

from abc import ABCMeta, abstractmethod


class ITunnel(object):
    """Interface for a tunnelling object."""

    @abstractmethod
    def __init__(self, src_sock, dst_sock):
        """
        Initialize object's source and destination sockets.

        Args:
            src_sock (Socket): Input socket for the tunnel objcect.
            dst_sock (Socket): Output socket for the tunnel object.

        Raises:
            NotImplementedError: Abstract method.

        """
        raise NotImplementedError

    @abstractmethod
    def start_tunneling(self):
        """
        Start tunneling.

        Raises:
            NotImplementedError: Abstract method.

        """
        raise NotImplementedError
