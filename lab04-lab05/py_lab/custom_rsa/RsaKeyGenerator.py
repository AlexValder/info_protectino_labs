from .RandomPrimeNumberGenerator import RandomPrimeNumbersGenerator as rpng


class RsaKeyGenerator:
    '''This class encrypts data with RSA algorithm'''

    openedExponent: int

    def __init__(self):
        self.openedExponent = 65537 # Fifth Fermat's number


    def _extendedEuklidAlgorithm(self, modulo):
        eCopy = self.openedExponent
        x0 = 1; x1 = 0
        moduloCopy = modulo
        prevIterRest = moduloCopy // eCopy
        while True:
            eCopy %= moduloCopy
            if eCopy == 0:
                if moduloCopy != 1:
                    raise RuntimeError('Bad modulo')
                return x1 % modulo
            x1, x0 = x0 - prevIterRest * x1, x1
            prevIterRest = moduloCopy // eCopy
            eCopy, moduloCopy = moduloCopy, eCopy


    def getPrivateAndPublickKey(self):
        random1 = rpng.getRandomNumber(1024)
        random2 = rpng.getRandomNumber(1024)
        mul = random1 * random2
        eulerValue = (random1 - 1) * (random2 -1)
        privateExponent = self._extendedEuklidAlgorithm(eulerValue)
        if privateExponent * self.openedExponent % eulerValue != 1:
            raise RuntimeError('Bad private exponent.')
        return ((self.openedExponent, mul), (privateExponent, mul))
