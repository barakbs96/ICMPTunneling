"""Class SecureICMPSocke."""

from network.icmp_socket import ICMPSocket
from encryption.aes_encryptor import AESEncryptor


class SecureICMPSocket(ICMPSocket):
    """Secure socket object using icmp packets."""

    def __init__(self, ip='', port=0):
        """Initialize socket ip and port.

        Args:
            ip (str, optional): IP address which the socket will connect to or
            listen on.
            port (int, optional): Port number which the socket will connect to
            or listen on.
        """
        self._encryptor = AESEncryptor()
        super(SecureICMPSocket, self).__init__(ip, port)

    def recv(self, bufsize=0):
        """Recieve data over icmp packet and decrypt it.

        Args:
            bufsize (int): The maximum amount of data to be received at once.

        Returns:
            string: Decrypted received data.

        """
        data = super(SecureICMPSocket, self).recv()
        data = self._encryptor.decrypt(data)
        return data

    def send(self, data):
        """Encrypt data and send over ICMPSocket.

        Args:
            data (string): Data to send.
        """
        data = self._encryptor.encrypt(data)
        super(SecureICMPSocket, self).send(data)
