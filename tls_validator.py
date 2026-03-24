#!/usr/bin/env python3
"""HTTPS/TLS Configuration Validator"""

import ssl
import socket
from datetime import datetime


class TLSValidator:
    @staticmethod
    def check_ssl_certificate(hostname, port=443):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        "valid": True,
                        "subject": cert.get("subject", []),
                        "issuer": cert.get("issuer", []),
                        "version": ssock.version()
                    }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e)
            }

    @staticmethod
    def get_tls_version(hostname, port=443):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    return ssock.version()
        except Exception as e:
            return None

    @staticmethod
    def validate_ciphers(hostname, port=443):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cipher = ssock.cipher()
                    return {
                        "cipher_name": cipher[0],
                        "protocol": cipher[1],
                        "bits": cipher[2]
                    }
        except Exception as e:
            return {"error": str(e)}
