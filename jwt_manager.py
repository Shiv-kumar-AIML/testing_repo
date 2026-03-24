#!/usr/bin/env python3
"""JWT Token Manager"""

import json
import base64
import hashlib
import hmac
from datetime import datetime, timedelta


class JWTTokenManager:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    def encode_token(self, payload, expires_in=3600):
        header = {"alg": "HS256", "typ": "JWT"}
        
        current_time = datetime.now()
        payload["iat"] = int(current_time.timestamp())
        payload["exp"] = int((current_time + timedelta(seconds=expires_in)).timestamp())
        
        header_encoded = base64.urlsafe_b64encode(
            json.dumps(header).encode()
        ).decode().rstrip("=")
        
        payload_encoded = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).decode().rstrip("=")
        
        signature = hmac.new(
            self.secret_key.encode(),
            f"{header_encoded}.{payload_encoded}".encode(),
            hashlib.sha256
        ).digest()
        
        signature_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")
        
        return f"{header_encoded}.{payload_encoded}.{signature_encoded}"

    def decode_token(self, token):
        try:
            parts = token.split(".")
            
            if len(parts) != 3:
                return {"valid": False, "error": "Invalid token format"}
            
            header_encoded, payload_encoded, signature_encoded = parts
            
            signature_expected = hmac.new(
                self.secret_key.encode(),
                f"{header_encoded}.{payload_encoded}".encode(),
                hashlib.sha256
            ).digest()
            
            signature_expected_encoded = base64.urlsafe_b64encode(
                signature_expected
            ).decode().rstrip("=")
            
            if signature_expected_encoded != signature_encoded:
                return {"valid": False, "error": "Invalid signature"}
            
            padding = 4 - len(payload_encoded) % 4
            if padding != 4:
                payload_encoded += "=" * padding
            
            payload = json.loads(
                base64.urlsafe_b64decode(payload_encoded)
            )
            
            if payload["exp"] < datetime.now().timestamp():
                return {"valid": False, "error": "Token expired"}
            
            return {"valid": True, "payload": payload}
        except Exception as e:
            return {"valid": False, "error": str(e)}

    def verify_token(self, token):
        result = self.decode_token(token)
        return result["valid"]
