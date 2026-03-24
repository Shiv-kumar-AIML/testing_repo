#!/usr/bin/env python3
"""HTTP Security Headers Validator"""

import requests


class SecurityHeadersValidator:
    REQUIRED_HEADERS = {
        "Strict-Transport-Security": "max-age=31536000",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Content-Security-Policy": "default-src 'self'",
        "X-XSS-Protection": "1; mode=block"
    }

    @staticmethod
    def check_headers(url):
        try:
            response = requests.head(url, timeout=5)
            headers = response.headers
            
            results = {}
            for header, expected_value in SecurityHeadersValidator.REQUIRED_HEADERS.items():
                if header in headers:
                    results[header] = {
                        "present": True,
                        "value": headers[header]
                    }
                else:
                    results[header] = {
                        "present": False,
                        "value": None
                    }
            
            return results
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_security_score(headers_check):
        if "error" in headers_check:
            return 0
        
        total = len(SecurityHeadersValidator.REQUIRED_HEADERS)
        present = sum(1 for h in headers_check.values() if h["present"])
        
        return (present / total) * 100

    @staticmethod
    def missing_headers(headers_check):
        if "error" in headers_check:
            return []
        
        return [
            header for header, data in headers_check.items()
            if not data["present"]
        ]
