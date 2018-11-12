from Crypto.Cipher import AES
import base64

PRIVATE_SECRET_KEY = '/^;<90Bo5r;.P[xlg4:58O`,EAQQ3?,1'


class Crypto(object):
    """
    A crypto engine that provides encryption and decryption of passwords
    stored in the database. It uses a AES algorithm to ensure password
    security and strong cryptography.
    """

    def __init__(self, key: str = PRIVATE_SECRET_KEY) -> None:
        self.bs = 16
        self.cipher = AES.new(key, AES.MODE_ECB)

    def _pad(self, text: str) -> str:
        return text + (self.bs - len(text) % self.bs) * chr(self.bs - len(text) % self.bs)

    def _unpad(self, text: str) -> str:
        return text[:-ord(text[len(text) - 1:])]

    def encrypt(self, password: str) -> str:
        encrypted = self.cipher.encrypt(self._pad(password))
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    def decrypt(self, password: str) -> str:
        decoded = base64.b64decode(password)
        decrypted = self.cipher.decrypt(decoded)
        return str(self._unpad(decrypted), 'utf-8')
