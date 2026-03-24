#!/usr/bin/env python3
"""Environment Variable Security Manager"""

import os
from typing import Optional, Dict


class EnvSecurityManager:
    def __init__(self):
        self.required_vars = []
        self.sensitive_vars = []

    def require_env_var(self, var_name, description=""):
        self.required_vars.append({
            "name": var_name,
            "description": description
        })

    def mark_sensitive(self, var_name):
        self.sensitive_vars.append(var_name)

    def validate_environment(self):
        missing = []
        
        for var in self.required_vars:
            if var["name"] not in os.environ:
                missing.append(var["name"])
        
        return {
            "valid": len(missing) == 0,
            "missing": missing,
            "total_required": len(self.required_vars)
        }

    def get_env_var(self, var_name, default=None):
        value = os.environ.get(var_name, default)
        
        if value is None:
            raise ValueError(f"Environment variable {var_name} not found")
        
        return value

    def check_sensitive_vars_present(self):
        present = []
        missing = []
        
        for var in self.sensitive_vars:
            if var in os.environ:
                present.append(var)
            else:
                missing.append(var)
        
        return {
            "present": present,
            "missing": missing,
            "all_configured": len(missing) == 0
        }

    def get_safe_env_dump(self):
        safe_vars = {}
        
        for key, value in os.environ.items():
            if key in self.sensitive_vars:
                safe_vars[key] = "***REDACTED***"
            else:
                safe_vars[key] = value
        
        return safe_vars
