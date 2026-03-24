#!/usr/bin/env python3
"""Admin Access Validator"""

from datetime import datetime, timedelta


class AdminValidator:
    def __init__(self):
        self.admin_users = set()
        self.admin_logs = []
        self.failed_attempts = {}

    def add_admin(self, user_id):
        self.admin_users.add(user_id)
        self.admin_logs.append({
            "action": "ADD_ADMIN",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        })

    def remove_admin(self, user_id):
        if user_id in self.admin_users:
            self.admin_users.discard(user_id)
            self.admin_logs.append({
                "action": "REMOVE_ADMIN",
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            })
            return True
        return False

    def is_admin(self, user_id):
        return user_id in self.admin_users

    def log_admin_action(self, admin_id, action, resource):
        self.admin_logs.append({
            "admin_id": admin_id,
            "action": action,
            "resource": resource,
            "timestamp": datetime.now().isoformat()
        })

    def verify_admin_access(self, user_id, action):
        if not self.is_admin(user_id):
            self.track_failed_attempt(user_id)
            return False
        
        self.log_admin_action(user_id, action, "system")
        return True

    def track_failed_attempt(self, user_id):
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = []
        
        self.failed_attempts[user_id].append(datetime.now())

    def get_failed_attempts(self, user_id, minutes=60):
        if user_id not in self.failed_attempts:
            return 0
        
        cutoff = datetime.now() - timedelta(minutes=minutes)
        return sum(
            1 for attempt in self.failed_attempts[user_id]
            if attempt > cutoff
        )
