from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

class DESManager:
    def __init__(self, key_string):
        self.key = self._adjust_key(key_string)
        self.cipher = DES.new(self.key, DES.MODE_ECB)

    def _adjust_key(self, key_string):
        k = key_string.encode('utf-8')
        return k.ljust(8, b' ')[0:8]

    def encrypt(self, plain_text):
        padded_text = pad(plain_text.encode('utf-8'), DES.block_size)
        encrypted_bytes = self.cipher.encrypt(padded_text)
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, encrypted_text):
        try:
            encrypted_bytes = base64.b64decode(encrypted_text)
            decrypted_padded = self.cipher.decrypt(encrypted_bytes)
            return unpad(decrypted_padded, DES.block_size).decode('utf-8')
        except Exception as e:
            return f"[Şifre Çözülemedi: {str(e)}]"