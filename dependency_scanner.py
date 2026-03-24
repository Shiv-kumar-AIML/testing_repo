#!/usr/bin/env python3
"""Dependency Vulnerability Scanner"""

import json


class DependencyVulnerabilityScanner:
    def __init__(self):
        self.known_vulnerabilities = {
            "requests": ["2.28.0", "2.27.1"],
            "django": ["3.2.5", "3.1.0"],
            "flask": ["2.0.1", "1.1.2"],
            "urllib3": ["1.26.5", "1.26.4"],
            "pillow": ["8.3.1", "8.2.0"]
        }
        self.installed_packages = {}

    def add_known_vulnerability(self, package_name, versions):
        self.known_vulnerabilities[package_name] = versions

    def register_installed_package(self, package_name, version):
        self.installed_packages[package_name] = version

    def scan_package(self, package_name, version):
        if package_name not in self.known_vulnerabilities:
            return {"vulnerable": False, "reason": "No known vulnerabilities"}
        
        if version in self.known_vulnerabilities[package_name]:
            return {
                "vulnerable": True,
                "package": package_name,
                "version": version,
                "message": f"Vulnerability found in {package_name} {version}"
            }
        
        return {"vulnerable": False, "reason": "Version is safe"}

    def scan_all_installed(self):
        results = []
        for package, version in self.installed_packages.items():
            result = self.scan_package(package, version)
            if result["vulnerable"]:
                results.append(result)
        
        return results

    def get_security_report(self):
        vulnerabilities = self.scan_all_installed()
        total_packages = len(self.installed_packages)
        vulnerable_count = len(vulnerabilities)
        
        return {
            "total_packages": total_packages,
            "vulnerable_packages": vulnerable_count,
            "security_score": ((total_packages - vulnerable_count) / total_packages * 100) if total_packages > 0 else 0,
            "vulnerabilities": vulnerabilities
        }
