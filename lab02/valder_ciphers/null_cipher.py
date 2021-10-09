from .cipher import Cipher


class NullCipher(Cipher):
    def encode(self, raw: str) -> str:
        return raw

    def decode(self, raw: str) -> str:
        return raw
