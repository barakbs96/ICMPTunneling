class ISocket(object):
    def bind(self):
        """Summary
        bind to socket 
        
        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError

    def accept(self):
        """Summary
        Filter ICMP packets
        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError

    def connect(self):
        """Summary
        
        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError

    def send(self, data):
        """Summary
        Send data to the socket.
        Args:
            data (Byte): data to send
        
        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError

    def recv(self, amount):
        """Summary
        Receive data from socket
        Args:
            amount (Int): the maximum data to be received at once.
        
        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError