class Cipher:
    """Base class for custom ciphers."""
    def encode(self, raw: str) -> str:
        pass

    def decode(self, raw: str) -> str:
        pass
