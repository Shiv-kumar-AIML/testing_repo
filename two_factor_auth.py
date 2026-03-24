#!/usr/bin/env python3
"""Two-Factor Authentication Manager"""

import secrets
import time
from datetime import datetime, timedelta


class TwoFactorAuth:
    def __init__(self, otp_validity=300):
        self.otp_codes = {}
        self.otp_validity = otp_validity
        self.recovery_codes = {}

    def generate_otp(self, user_id):
        otp = str(secrets.randbelow(1000000)).zfill(6)
        
        self.otp_codes[user_id] = {
            "code": otp,
            "created_at": time.time(),
            "attempts": 0
        }
        
        return otp

    def verify_otp(self, user_id, otp):
        if user_id not in self.otp_codes:
            return False
        
        otp_data = self.otp_codes[user_id]
        
        if time.time() - otp_data["created_at"] > self.otp_validity:
            del self.otp_codes[user_id]
            return False
        
        if otp_data["attempts"] >= 3:
            del self.otp_codes[user_id]
            return False
        
        if otp_data["code"] != otp:
            otp_data["attempts"] += 1
            return False
        
        del self.otp_codes[user_id]
        return True

    def generate_recovery_codes(self, user_id, count=10):
        codes = [secrets.token_hex(4) for _ in range(count)]
        self.recovery_codes[user_id] = codes
        return codes

    def verify_recovery_code(self, user_id, code):
        if user_id not in self.recovery_codes:
            return False
        
        if code in self.recovery_codes[user_id]:
            self.recovery_codes[user_id].remove(code)
            return True
        
        return False
