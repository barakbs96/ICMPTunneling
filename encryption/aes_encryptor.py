"""Class AESEncryptor."""
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from encryption.iencryptor import IEncryptor
from config.encryption.aes import ENCRYPTION_KEY, BLOCK_SIZE


class AESEncryptor(IEncryptor):
    """Enecyptor using AES, implements iencryptor."""

    def encrypt(self, data):
        """Encrypt data using AES.

        Args:
            data (string): Data to encrypt.

        Returns:
            string: Encrypted data.

        """
        padded_data = self._pad(data)
        iv = Random.new().read(BLOCK_SIZE)
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(padded_data))

    def decrypt(self, data):
        """Decrypt data using AES.

        Args:
            data (string): Data to decrypt.

        Returns:
            string: Decrypted data.

        """
        data = base64.b64decode(data)
        iv = data[:BLOCK_SIZE]
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(data[BLOCK_SIZE:]))

    def _pad(self, data):
        """Pad data to Block size.

        Args:
            data (string): Data to pad.

        Returns:
            string: Padded data.

        """
        return data + ((BLOCK_SIZE - len(data) % BLOCK_SIZE) *
                       chr(BLOCK_SIZE - len(data) % BLOCK_SIZE))

    def _unpad(self, data):
        """Remove padding from data.

        Args:
            data (string): Data to unpad.

        Returns:
            string: Unpadded data.

        """
        return data[:-ord(data[len(data)-1:])]
