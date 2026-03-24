#!/usr/bin/env python3
"""Request Validator"""

import re
from urllib.parse import urlparse


class RequestValidator:
    def __init__(self):
        self.allowed_methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
        self.blocked_ips = []
        self.rate_limits = {}

    def validate_http_method(self, method):
        return method.upper() in self.allowed_methods

    def add_allowed_method(self, method):
        self.allowed_methods.append(method.upper())

    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme in ["http", "https"], result.netloc])
        except:
            return False

    def block_ip(self, ip_address):
        if ip_address not in self.blocked_ips:
            self.blocked_ips.append(ip_address)

    def is_ip_blocked(self, ip_address):
        return ip_address in self.blocked_ips

    def validate_request_headers(self, headers):
        if not isinstance(headers, dict):
            return False
        
        required = ["Host", "User-Agent"]
        return all(header in headers for header in required)

    def extract_ip_from_headers(self, headers):
        if "X-Forwarded-For" in headers:
            return headers["X-Forwarded-For"].split(",")[0].strip()
        return headers.get("Remote-Addr", None)

    def validate_content_length(self, content_length, max_length=10485760):
        try:
            return int(content_length) <= max_length
        except:
            return False
