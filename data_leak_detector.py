#!/usr/bin/env python3
"""Data Leak Detection System"""

import re
from datetime import datetime


class DataLeakDetector:
    def __init__(self):
        self.patterns = {
            "api_key": r"(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9_\-]{20,}",
            "password": r"(?i)(password|passwd|pwd)['\"]?\s*[:=]\s*['\"]?[^\s]+",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
            "social_security": r"\b\d{3}-\d{2}-\d{4}\b",
            "database_uri": r"(?i)(mongodb|mysql|postgresql)://[^\s]+"
        }
        self.leaks = []

    def scan_text(self, text, source="unknown"):
        findings = []
        
        for leak_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                findings.append({
                    "type": leak_type,
                    "value": match.group(),
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                })
                self.leaks.append(findings[-1])
        
        return findings

    def scan_file(self, filepath):
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return self.scan_text(content, filepath)
        except Exception as e:
            return {"error": str(e)}

    def get_leak_summary(self):
        summary = {}
        for leak in self.leaks:
            leak_type = leak["type"]
            summary[leak_type] = summary.get(leak_type, 0) + 1
        
        return {
            "total_leaks": len(self.leaks),
            "by_type": summary,
            "leaks": self.leaks
        }

    def clear_leaks(self):
        self.leaks = []
