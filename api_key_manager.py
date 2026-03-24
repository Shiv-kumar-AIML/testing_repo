#!/usr/bin/env python3
"""API Key Manager"""

import secrets
import hashlib
from datetime import datetime


class APIKeyManager:
    def __init__(self):
        self.keys = {}

    def generate_key(self, name):
        key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        self.keys[key_hash] = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        
        return key

    def validate_key(self, key):
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        if key_hash not in self.keys:
            return False
        
        return self.keys[key_hash]["active"]

    def revoke_key(self, key):
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        if key_hash in self.keys:
            self.keys[key_hash]["active"] = False
            return True
        return False

    def list_keys(self):
        return [
            {"hash": k, "name": v["name"], "active": v["active"]}
            for k, v in self.keys.items()
        ]
