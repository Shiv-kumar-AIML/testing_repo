#!/usr/bin/env python3
"""
Security Testing Utilities - Security Scanning and Validation Tools

This module provides utilities for testing, validating, and scanning code
for common security vulnerabilities and best practices.
"""

import re
import hashlib
import secrets
from typing import List, Dict, Tuple, Optional
from pathlib import Path


# ============================================================================
# 1. CODE PATTERN SCANNING UTILITIES
# ============================================================================

class SecurityScanner:
    """Scans code for common security anti-patterns and vulnerabilities."""
    
    # Vulnerable patterns to detect
    VULNERABLE_PATTERNS = {
        "sql_injection": [
            r"f[\'\"].*SELECT.*{.*}",  # f-string with SQL
            r"\.execute\s*\(\s*f[\'\"]",  # execute with f-string
            r"query\s*=\s*f[\'\"]",  # query with f-string
        ],
        "command_injection": [
            r"subprocess\.(call|run|Popen)\s*\(\s*[^\[,]*\+",  # subprocess with concatenation
            r"os\.(system|popen)\s*\(\s*f[\'\"]",  # os.system with f-string
        ],
        "hardcoded_secrets": [
            r"(password|passwd|pwd|api_key|secret|token)\s*=\s*[\'\"][\w\.\-\/\+]+[\'\"]",
            r"(API_KEY|SECRET|TOKEN|PASSWORD)\s*=\s*[\'\"]",
        ],
        "pickle_usage": [
            r"pickle\.(loads|load)\s*\(\s*\w+",  # pickle with untrusted data
        ],
    }
    
    @staticmethod
    def scan_file(filepath: str) -> Dict[str, List[Tuple[int, str]]]:
        """
        Scan a Python file for security vulnerabilities.
        
        Args:
            filepath: Path to the Python file to scan
            
        Returns:
            Dictionary with vulnerability types and their locations
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return {"error": [(0, str(e))]}
        
        findings = {}
        
        for vuln_type, patterns in SecurityScanner.VULNERABLE_PATTERNS.items():
            findings[vuln_type] = []
            
            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        findings[vuln_type].append((line_num, line.strip()))
        
        # Remove empty entries
        return {k: v for k, v in findings.items() if v}
    
    @staticmethod
    def report_findings(findings: Dict[str, List[Tuple[int, str]]]) -> str:
        """
        Generate a readable report of security findings.
        
        Args:
            findings: Vulnerability findings from scan_file()
            
        Returns:
            Formatted report string
        """
        if not findings:
            return "✓ No vulnerabilities detected!"
        
        report = ["SECURITY SCAN REPORT", "=" * 70]
        
        for vuln_type, locations in findings.items():
            report.append(f"\n{vuln_type.upper().replace('_', ' ')}")
            report.append("-" * 70)
            for line_num, line_content in locations:
                report.append(f"  Line {line_num}: {line_content}")
        
        return "\n".join(report)


# ============================================================================
# 2. PASSWORD & CREDENTIALS VALIDATION
# ============================================================================

class PasswordValidator:
    """Validates password strength and security requirements."""
    
    @staticmethod
    def check_strength(password: str) -> Dict[str, any]:
        """
        Check password strength against security criteria.
        
        Args:
            password: Password to evaluate
            
        Returns:
            Dictionary with strength assessment
        """
        checks = {
            "length": len(password) >= 12,
            "uppercase": bool(re.search(r"[A-Z]", password)),
            "lowercase": bool(re.search(r"[a-z]", password)),
            "numbers": bool(re.search(r"\d", password)),
            "special": bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};:'\",.<>?/\\|`~]", password)),
        }
        
        strength_score = sum(checks.values())
        
        if strength_score >= 5:
            strength = "STRONG"
        elif strength_score >= 3:
            strength = "MODERATE"
        else:
            strength = "WEAK"
        
        return {
            "strength": strength,
            "score": strength_score,
            "checks": checks,
        }
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """
        Generate a cryptographically secure random password.
        
        Args:
            length: Length of the password (minimum 12)
            
        Returns:
            Secure random password
        """
        if length < 12:
            length = 12
        
        # Ensure password has all character types
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
        password = [
            secrets.choice("abcdefghijklmnopqrstuvwxyz"),
            secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            secrets.choice("0123456789"),
            secrets.choice("!@#$%^&*"),
        ]
        
        # Fill remaining length with random characters
        password += [secrets.choice(chars) for _ in range(length - 4)]
        
        # Shuffle to avoid predictable pattern
        import random
        random.shuffle(password)
        
        return "".join(password)


# ============================================================================
# 3. INPUT VALIDATION UTILITIES
# ============================================================================

class InputValidator:
    """Validates and sanitizes user input."""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """Validate phone number format."""
        pattern = r"^\+?1?\d{9,15}$"
        return bool(re.match(pattern, phone.replace("-", "").replace(" ", "")))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format."""
        pattern = r"^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}.*$"
        return bool(re.match(pattern, url))
    
    @staticmethod
    def sanitize_sql_input(user_input: str) -> str:
        """
        Basic SQL input sanitization (use parameterized queries instead!).
        
        Args:
            user_input: Raw user input
            
        Returns:
            Sanitized input
        """
        # THIS IS NOT A REPLACEMENT FOR PARAMETERIZED QUERIES!
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
        sanitized = user_input
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, "")
        
        return sanitized
    
    @staticmethod
    def sanitize_html_input(user_input: str) -> str:
        """Escape HTML special characters."""
        replacements = {
            "<": "&lt;",
            ">": "&gt;",
            '"': "&quot;",
            "'": "&#x27;",
            "&": "&amp;",
        }
        
        result = user_input
        for char, escape in replacements.items():
            result = result.replace(char, escape)
        
        return result


# ============================================================================
# 4. CRYPTOGRAPHIC UTILITIES
# ============================================================================

class CryptoUtils:
    """Provides cryptographic utilities for secure operations."""
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Dict[str, str]:
        """
        Hash a password using PBKDF2 (simplified - use bcrypt/argon2 in production).
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Dictionary with hash and salt
        """
        if not salt:
            salt = secrets.token_hex(16)
        
        # Use PBKDF2 with 100,000 iterations
        hash_obj = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        hash_value = hash_obj.hex()
        
        return {
            "hash": hash_value,
            "salt": salt,
            "algorithm": "pbkdf2_sha256",
            "iterations": 100000,
        }
    
    @staticmethod
    def verify_password(password: str, stored_hash: str, salt: str) -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password: Password to verify
            stored_hash: Stored hash value
            salt: Salt used for hashing
            
        Returns:
            True if password matches, False otherwise
        """
        hash_result = CryptoUtils.hash_password(password, salt)
        return hash_result["hash"] == stored_hash
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.
        
        Args:
            length: Length of token in bytes
            
        Returns:
            Hex-encoded random token
        """
        return secrets.token_hex(length)


# ============================================================================
# 5. SECURITY AUDIT CHECKLIST
# ============================================================================

class SecurityChecklist:
    """Security best practices checklist."""
    
    CHECKLIST_ITEMS = {
        "authentication": [
            "Use strong password requirements (min 12 characters)",
            "Implement multi-factor authentication (MFA)",
            "Never store passwords in plain text",
            "Use secure password hashing (bcrypt, argon2)",
            "Implement account lockout after failed attempts",
        ],
        "authorization": [
            "Implement role-based access control (RBAC)",
            "Follow principle of least privilege",
            "Validate permissions on every request",
            "Log authorization failures",
        ],
        "data_security": [
            "Encrypt sensitive data at rest (AES-256)",
            "Use HTTPS/TLS for data in transit",
            "Implement proper data retention policies",
            "Sanitize and validate all user input",
            "Use parameterized queries for database operations",
        ],
        "error_handling": [
            "Don't expose sensitive info in error messages",
            "Implement comprehensive logging",
            "Monitor for security anomalies",
            "Have incident response plan",
        ],
        "dependencies": [
            "Keep dependencies up to date",
            "Scan for known vulnerabilities (pip-audit)",
            "Use dependency pinning",
            "Review security advisories regularly",
        ],
    }
    
    @staticmethod
    def generate_audit_report() -> str:
        """Generate a security audit checklist report."""
        report = ["SECURITY AUDIT CHECKLIST", "=" * 70]
        
        for category, items in SecurityChecklist.CHECKLIST_ITEMS.items():
            report.append(f"\n{category.upper().replace('_', ' ')}")
            report.append("-" * 70)
            for i, item in enumerate(items, 1):
                report.append(f"  [ ] {item}")
        
        return "\n".join(report)


# ============================================================================
# DEMONSTRATION & TESTING
# ============================================================================

def demonstrate_utilities():
    """Demonstrate all security utilities."""
    print("=" * 70)
    print("SECURITY TESTING UTILITIES - DEMONSTRATION")
    print("=" * 70)
    
    # Password validation
    print("\n1. PASSWORD VALIDATION")
    print("-" * 70)
    test_passwords = ["weak", "Better123!", "SuperSecure@2024!#"]
    
    for pwd in test_passwords:
        result = PasswordValidator.check_strength(pwd)
        print(f"Password: '{pwd}'")
        print(f"  Strength: {result['strength']} ({result['score']}/5)")
    
    print(f"\nGenerated Secure Password: {PasswordValidator.generate_secure_password()}")
    
    # Input validation
    print("\n2. INPUT VALIDATION")
    print("-" * 70)
    print(f"  Valid email 'test@example.com': {InputValidator.validate_email('test@example.com')}")
    print(f"  Valid URL 'https://example.com': {InputValidator.validate_url('https://example.com')}")
    print(f"  Valid phone '+1234567890': {InputValidator.validate_phone('+1234567890')}")
    
    # Cryptographic utilities
    print("\n3. CRYPTOGRAPHIC UTILITIES")
    print("-" * 70)
    password = "MySecurePassword123!"
    hash_result = CryptoUtils.hash_password(password)
    print(f"Password: {password}")
    print(f"Hash: {hash_result['hash'][:32]}...")
    print(f"Verification: {CryptoUtils.verify_password(password, hash_result['hash'], hash_result['salt'])}")
    print(f"Generated Token: {CryptoUtils.generate_token(16)}")
    
    # Security checklist
    print("\n4. SECURITY AUDIT CHECKLIST")
    print("-" * 70)
    print(SecurityChecklist.generate_audit_report())


if __name__ == "__main__":
    demonstrate_utilities()
