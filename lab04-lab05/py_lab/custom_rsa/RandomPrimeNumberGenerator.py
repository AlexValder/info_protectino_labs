import random

    
class RandomPrimeNumbersGenerator:
    '''This class helps you to generate big prime numbers.'''

    @staticmethod
    def _isPrime(number: int, testCount:int = 128) -> bool:
        #This method is taken from here: https://medium.com/@prudywsh/how-to-generate-big-prime-numbers-miller-rabin-49e6e6af32fb
        if number == 2 or number == 3:
            return True
        if number <= 1 or number % 2 == 0:
            return False
        s = 0
        r = number - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        for _ in range(testCount):
            randomRange = random.randrange(2, number - 1)
            x = pow(randomRange, r, number)
            if x != 1 and x != number - 1:
                j = 1
                while j < s and x != number - 1:
                    x = pow(x, 2, number)
                    if x == 1:
                        return False
                    j += 1
                if x != number - 1:
                    return False
        return True

    
    @staticmethod
    def getRandomNumber(bitLength: int) -> int:
        while True:
            randomNumber = random.getrandbits(bitLength)
            randomNumber |= (1 << bitLength - 1) | 1
            if (RandomPrimeNumbersGenerator._isPrime(randomNumber)):
                return randomNumber
