#!/usr/bin/env python3
"""Data Encryption Utility"""

import base64
from cryptography.fernet import Fernet


class EncryptionUtil:
    def __init__(self, key=None):
        if key is None:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)
        self.key = key

    def get_key(self):
        return self.key.decode()

    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.cipher.encrypt(data)
        return encrypted.decode()

    def decrypt(self, encrypted_data):
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode()

    def encrypt_dict(self, data_dict):
        import json
        json_str = json.dumps(data_dict)
        return self.encrypt(json_str)

    def decrypt_dict(self, encrypted_data):
        import json
        decrypted_str = self.decrypt(encrypted_data)
        return json.loads(decrypted_str)
