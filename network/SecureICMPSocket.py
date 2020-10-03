from network.ICMPSocket import ICMPSocket
from encryption.AESEncryptor import AESEncryptor

class SecureICMPSocket(ICMPSocket):
    def __init__(self, ip='', port=0):
        self._encryptor = AESEncryptor()
        super(SecureICMPSocket, self).__init__(ip, port)

    def send(self, data):
        data = self._encryptor.encrypt(data)
        super(SecureICMPSocket, self).send(data)

    def recv(self, amount=0):
        data = super(SecureICMPSocket, self).recv()
        data = self._encryptor.decrypt(data)
        return data
