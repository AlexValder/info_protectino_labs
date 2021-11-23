import hashlib
import sys


class RsaValidator:
    def __init__(self):
        self._validatingKey = None
        self._signingKey = None


    def setValidatingKey(self, publicKeyFilePath: str) -> None:
        with open(publicKeyFilePath, 'r', encoding='utf8') as publicKey:
            rawKey = publicKey.readlines()
            self._validatingKey = (int(rawKey[0]), int(rawKey[1]))


    def setSigningKey(self, privateKeyFilePath: str) -> None:
        with open(privateKeyFilePath, 'r', encoding='utf8') as privateKey:
            rawKey = privateKey.readlines()
            self._signingKey = (int(rawKey[0]), int(rawKey[1]))


    def signFile(self, fileToSignPath: str) -> None:
        if self._signingKey is None:
            raise RuntimeError('Signing (private) key is not set.')
        
        with open(fileToSignPath, 'rb') as fileToSign, open(fileToSignPath + '.signed', 'wb') as signedFile:
            fileBytes = fileToSign.read()
            fileHash = int.from_bytes(hashlib.sha256(fileBytes).digest(), sys.byteorder)
            encryptedHash = pow(fileHash, self._signingKey[0], self._signingKey[1])
            encryptedHashBytes = encryptedHash.to_bytes((encryptedHash.bit_length() + 7) // 8, sys.byteorder)
            encryptedHashBytes += b'\0' * (256 - len(encryptedHashBytes))
            fileBytes += encryptedHashBytes
            signedFile.write(b'\xbd\xef\xc2YBk\xd0\x86\xd1\x12a\x08\xac9U\xa6\xc1Qd\xca\x1fY\x1e\x08r\xec|I\xe4@.j')
            signedFile.write(fileBytes)


    def validateFile(self, fileToValidatePath: str) -> bool:
        if self._validatingKey is None:
            raise RuntimeError('Validating (public) key is not set.')
        
        with open(fileToValidatePath, 'rb') as fileToValidate, open(fileToValidatePath.removesuffix('.signed'), 'wb') as validatedFile:
            toValidateBytes = fileToValidate.read()
            
            if len(toValidateBytes) <= 32 or toValidateBytes[:32] != b'\xbd\xef\xc2YBk\xd0\x86\xd1\x12a\x08\xac9U\xa6\xc1Qd\xca\x1fY\x1e\x08r\xec|I\xe4@.j':
                raise RuntimeError('File is not signed.')
            
            fileItself = toValidateBytes[32:-256]
            fileHash = int.from_bytes(hashlib.sha256(fileItself).digest(), sys.byteorder)
            
            encryptedHash = int.from_bytes(toValidateBytes[-256:], sys.byteorder)
            decryptedHash = pow(encryptedHash, self._validatingKey[0], self._validatingKey[1])
            validatedFile.write(fileItself)
            return decryptedHash == fileHash
