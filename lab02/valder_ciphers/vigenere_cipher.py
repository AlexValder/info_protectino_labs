from string import ascii_lowercase, ascii_uppercase
from typing import List

from .cipher import Cipher


class KeywordNotFoundError(Exception):
    """Error for indicating that keyword was changed before decrypting"""
    def __init__(self):
        super().__init__("Keyword is absent")


class VigenereCipher(Cipher):
    __key: str
    __keyword: str
    __alpha_len: int
    __lower: str
    __upper: str

    def __init__(
            self,
            keyword: str,
            lowercase_alphabet: str = ascii_lowercase,
            uppercase_alphabet: str = ascii_uppercase,
    ):
        super()
        self.__keyword = keyword
        self.__key = ""
        self.__lower = lowercase_alphabet
        self.__upper = uppercase_alphabet
        self.__alpha_len = len(lowercase_alphabet)
        assert (self.__alpha_len == len(uppercase_alphabet))

    @property
    def key(self) -> str:
        return self.__key

    @key.setter
    def key(self, new_key: str):
        if new_key and not new_key.isspace():
            self.__key = new_key
            self.__keyword = ""

    @property
    def keyword(self) -> str:
        return self.__keyword

    @keyword.setter
    def keyword(self, new_keyword: str):
        if new_keyword and not new_keyword.isspace():
            self.__keyword = new_keyword
            self.__key = ""

    def encode(self, raw: str) -> str:
        self.__key = self.__generate_key(raw, self.keyword)
        encrypted: List[str] = []
        for i, char in enumerate(raw):
            if not char.isalpha():
                encrypted.append(char)
            else:
                alphabet = self.__upper if char.isupper() else self.__lower
                encrypted.append(
                    alphabet[(self.__order(char) + self.__order(self.__key[i])) % self.__alpha_len]
                )
        return "".join(encrypted)

    def decode(self, raw: str) -> str:
        if not self.__key:
            raise KeywordNotFoundError
        return self.decode_with_key(raw, self.__key)

    def decode_with_key(self, raw: str, key: str) -> str:
        decoded: List[str] = []
        for i, char in enumerate(raw):
            if not char.isalpha():
                decoded.append(char)
            else:
                alphabet = self.__upper if char.isupper() else self.__lower
                decoded.append(
                    alphabet[
                        (self.__order(char) - self.__order(key[i]) + self.__alpha_len) % self.__alpha_len
                        ]
                )
        return "".join(decoded)

    def __order(self, char: str) -> int:
        assert (len(char) == 1)
        if char.isupper():
            return self.__upper.index(char)
        else:
            return self.__lower.index(char)

    @staticmethod
    def __generate_key(string: str, key: str) -> str:
        key = list(key)
        if len(string) == len(key):
            return key
        else:
            for i in range(len(string) - len(key)):
                key.append(key[i % len(key)])
        return "".join(key)
