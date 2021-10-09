from string import ascii_lowercase, ascii_uppercase
from typing import List

from .cipher import Cipher


class CaesarCipher(Cipher):
    shift: int
    alpha_len: int
    lower: str
    upper: str

    def __init__(
            self,
            shift: int,
            lowercase_alphabet: str = ascii_lowercase,
            uppercase_alphabet: str = ascii_uppercase,
    ):
        super()
        self.shift = shift
        self.lower = lowercase_alphabet
        self.upper = uppercase_alphabet
        self.alpha_len = len(lowercase_alphabet)
        assert(len(lowercase_alphabet) == len(uppercase_alphabet))

    def encode(self, raw: str) -> str:
        return self.__inner_caesar(raw, self.shift)

    def decode(self, raw: str) -> str:
        return self.__inner_caesar(raw, -self.shift)

    def __inner_caesar(self, _input: str, _shift: int) -> str:
        processed: List[str] = []
        for char in _input:
            if not char.isalpha():
                processed.append(char)
            else:
                alphabet = self.upper if char.isupper() else self.lower
                processed.append(alphabet[(alphabet.index(char) + _shift) % self.alpha_len])
        return "".join(processed)
