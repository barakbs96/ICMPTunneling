"""Test encryptor."""
import pytest

from encryption.aes_encryptor import AESEncryptor
from config.encryption.aes import BLOCK_SIZE


@pytest.fixture
def encryptor():
    """Return AESEncryptor instance.

    Returns:
        AESEncryptor: AESEncryptor instance.

    """
    return AESEncryptor()


def test_encrypt_decrypt(encryptor):
    """Test encrypt and decrypt of data.

    Args:
        encryptor (AESEncryptor): AESEncryptor instance.
    """
    data = 'abcdfghijkl'
    encrypted = encryptor.encrypt(data)
    assert data == encryptor.decrypt(encrypted)


def test_pad(encryptor):
    """Test padding of data to block size.

    Args:
        encryptor (AESEncryptor): AESEncryptor instance.
    """
    data = 'abc'
    padded = encryptor._pad(data)
    assert len(padded) == BLOCK_SIZE


def test_pad_unpad(encryptor):
    """Test Unpad of data.

    Args:
        encryptor (AESEncryptor): AESEncryptor instance.
    """
    data = 'abcdfghijkl'
    padded = encryptor._pad(data)
    assert data == encryptor._unpad(padded)
