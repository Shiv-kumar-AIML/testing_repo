#!/usr/bin/env python3
"""CSRF Token Generator"""

import secrets
import hashlib
from datetime import datetime, timedelta


class CSRFTokenManager:
    def __init__(self, token_lifetime=3600):
        self.tokens = {}
        self.token_lifetime = token_lifetime

    def generate_token(self, session_id):
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        self.tokens[token_hash] = {
            "session_id": session_id,
            "created_at": datetime.now(),
            "used": False
        }
        
        return token

    def validate_token(self, token, session_id):
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        
        if token_hash not in self.tokens:
            return False
        
        token_data = self.tokens[token_hash]
        
        if token_data["used"]:
            return False
        
        if datetime.now() - token_data["created_at"] > timedelta(seconds=self.token_lifetime):
            del self.tokens[token_hash]
            return False
        
        if token_data["session_id"] != session_id:
            return False
        
        token_data["used"] = True
        return True

    def cleanup_expired(self):
        expired_tokens = [
            token_hash for token_hash, data in self.tokens.items()
            if datetime.now() - data["created_at"] > timedelta(seconds=self.token_lifetime)
        ]
        for token in expired_tokens:
            del self.tokens[token]
