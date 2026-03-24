#!/usr/bin/env python3
"""Token Manager for Session Handling"""

import secrets
import time
from typing import Dict, Optional


class TokenManager:
    def __init__(self, token_lifetime=3600):
        self.token_lifetime = token_lifetime
        self.tokens = {}

    def generate_token(self, user_id):
        token = secrets.token_urlsafe(32)
        self.tokens[token] = {
            "user_id": user_id,
            "created_at": time.time()
        }
        return token

    def validate_token(self, token):
        if token not in self.tokens:
            return None
        
        token_data = self.tokens[token]
        created_at = token_data["created_at"]
        
        if time.time() - created_at > self.token_lifetime:
            del self.tokens[token]
            return None
        
        return token_data["user_id"]

    def revoke_token(self, token):
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False

    def revoke_user_tokens(self, user_id):
        tokens_to_remove = [
            token for token, data in self.tokens.items()
            if data["user_id"] == user_id
        ]
        for token in tokens_to_remove:
            del self.tokens[token]
        return len(tokens_to_remove)


if __name__ == "__main__":
    manager = TokenManager(token_lifetime=5)
    
    token1 = manager.generate_token("user1")
    token2 = manager.generate_token("user2")
    
    print(f"Token1 user: {manager.validate_token(token1)}")
    print(f"Token2 user: {manager.validate_token(token2)}")
    
    manager.revoke_token(token1)
    print(f"After revoke: {manager.validate_token(token1)}")
