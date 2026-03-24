#!/usr/bin/env python3
"""Input Sanitizer"""

import re


class InputSanitizer:
    @staticmethod
    def sanitize_username(username):
        if not isinstance(username, str):
            return None
        
        username = username.strip()
        if len(username) < 3 or len(username) > 50:
            return None
        
        if not re.match("^[a-zA-Z0-9_-]+$", username):
            return None
        
        return username

    @staticmethod
    def sanitize_email(email):
        if not isinstance(email, str):
            return None
        
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, email):
            return email.lower()
        return None

    @staticmethod
    def sanitize_filename(filename):
        filename = re.sub(r"[^\w\s.-]", "", filename)
        filename = filename.strip()
        return filename if filename else None

    @staticmethod
    def remove_sql_keywords(text):
        dangerous = ["DROP", "DELETE", "INSERT", "UPDATE", "SELECT", "EXEC"]
        for keyword in dangerous:
            text = re.sub(rf"\b{keyword}\b", "", text, flags=re.IGNORECASE)
        return text.strip()
