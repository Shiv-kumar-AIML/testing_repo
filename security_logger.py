#!/usr/bin/env python3
"""Simple Security Logger"""

import datetime
import json


class SecurityLogger:
    def __init__(self, log_file="security.log"):
        self.log_file = log_file

    def log_event(self, event_type, message, severity="INFO"):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "type": event_type,
            "message": message,
            "severity": severity
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    def log_login(self, user_id):
        self.log_event("LOGIN", f"User {user_id} logged in")

    def log_failed_login(self, user_id):
        self.log_event("FAILED_LOGIN", f"Failed login attempt for {user_id}", "WARNING")

    def log_access_denied(self, user_id, resource):
        self.log_event("ACCESS_DENIED", f"User {user_id} denied access to {resource}", "WARNING")

    def log_data_access(self, user_id, data_type):
        self.log_event("DATA_ACCESS", f"User {user_id} accessed {data_type}")


if __name__ == "__main__":
    logger = SecurityLogger()
    
    logger.log_login("user123")
    logger.log_failed_login("user456")
    logger.log_access_denied("user789", "admin_panel")
    logger.log_data_access("user123", "customer_database")
    
    print("Logs recorded in security.log")
