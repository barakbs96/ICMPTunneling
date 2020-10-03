import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from encryption.IEncryptor import IEncryptor
from config.encryption.aes import ENCRYPTION_KEY, BLOCK_SIZE

class AESEncryptor(IEncryptor):
    def encrypt(self, data):
        data = self._pad(data)
        iv = Random.new().read(BLOCK_SIZE)
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(data))

    def decrypt(self, data):
        data = base64.b64decode(data)
        iv = data[:BLOCK_SIZE]
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(data[BLOCK_SIZE:]))

    def _pad(self, data):
        return data + (BLOCK_SIZE - len(data) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(data) % BLOCK_SIZE)

    def _unpad(self, data):
        return data[:-ord(data[len(data)-1:])]