import sys
from typing import Tuple


class RsaCryptor:
    _pubKey: Tuple[int, int]
    _prvKey: Tuple[int, int]

    def __init__(self):
        self._pubKey = None
        self._prvKey = None


    def setEncryptionKey(self, publicKeyFilePath):
        with open(publicKeyFilePath, 'r', encoding='utf8') as publicKey:
            rawKey = publicKey.readlines()
            self._pubKey = (int(rawKey[0]), int(rawKey[1]))
    

    def setDecryptionKey(self, privateKeyFilePath: str):
        with open(privateKeyFilePath, 'r', encoding='utf8') as privateKey:
            rawKey = privateKey.readlines()
            self._prvKey = (int(rawKey[0]), int(rawKey[1]))


    def encrypt(self, blockOfBytes: bytes):
        if self._pubKey is None:
            raise RuntimeError('No encryption key set')
        message: int = int.from_bytes(blockOfBytes, sys.byteorder)
        encrypted: int = pow(message, self._pubKey[0], self._pubKey[1])
        return encrypted.to_bytes((encrypted.bit_length() + 7) // 8, sys.byteorder)


    def decrypt(self, blockOfBytes: bytes):
        if self._prvKey is None:
            raise RuntimeError('No decryption key set')
        message: int = int.from_bytes(blockOfBytes, sys.byteorder)
        decrypted: int = pow(message, self._prvKey[0], self._prvKey[1])
        res = decrypted.to_bytes((decrypted.bit_length() + 7) // 8, sys.byteorder)
        return res
