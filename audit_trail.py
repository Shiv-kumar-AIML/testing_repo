#!/usr/bin/env python3
"""Audit Trail Logger"""

import json
from datetime import datetime


class AuditTrail:
    def __init__(self, log_file="audit.log"):
        self.log_file = log_file

    def log_action(self, user_id, action, resource, status="SUCCESS"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "status": status
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def log_create(self, user_id, resource):
        self.log_action(user_id, "CREATE", resource)

    def log_read(self, user_id, resource):
        self.log_action(user_id, "READ", resource)

    def log_update(self, user_id, resource):
        self.log_action(user_id, "UPDATE", resource)

    def log_delete(self, user_id, resource):
        self.log_action(user_id, "DELETE", resource)
