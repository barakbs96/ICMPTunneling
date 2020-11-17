"""Class IEncryptor."""


class IEncryptor(object):
    """Interface for encryptor object."""

    def encrypt(self, data):
        """Encrypt data.

        Args:
            data (string): Data to encrypt.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError

    def decrypt(self, data):
        """Decrypt data.

        Args:
            data (string): Data to decrypt.

        Raises:
            NotImplementedError: Abstract Method.

        """
        raise NotImplementedError
