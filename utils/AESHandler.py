from utils import config
from Crypto.Cipher import AES


class AESHandler(object):
    source_key = config("SOURCE_SALT", cast=str).encode("utf-8")

    @staticmethod
    def pad(value):
        while len(value) % 16 != 0:
            value += b' '
        return value

    @staticmethod
    def encrypt(text):
        if isinstance(text, str): text = text.encode()
        _aes = AES.new(AESHandler.pad(AESHandler.source_key), AES.MODE_ECB)
        return _aes.encrypt(AESHandler.pad(text))

    @staticmethod
    def decrypt(encrypted_text):
        _aes = AES.new(AESHandler.pad(AESHandler.source_key), AES.MODE_ECB)
        return str(_aes.decrypt(encrypted_text), encoding='utf-8', errors="ignore")


if __name__ == "__main__":
    tt = "e846d98b059a1afaa6212864ac5b3bc40ddae9e8681df67e2abdc1e2094a075f".encode()
    tt_encrypt = AESHandler.encrypt(tt)
    print(tt_encrypt)
    tt2 = AESHandler.decrypt(tt_encrypt)
    print(tt2)

