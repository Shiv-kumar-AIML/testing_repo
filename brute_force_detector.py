#!/usr/bin/env python3
"""Brute Force Attack Detector"""

from datetime import datetime, timedelta
from collections import defaultdict


class BruteForceDetector:
    def __init__(self, max_attempts=5, lockout_duration=900):
        self.max_attempts = max_attempts
        self.lockout_duration = lockout_duration
        self.attempts = defaultdict(list)
        self.lockouts = {}

    def record_attempt(self, user_id):
        current_time = datetime.now()
        self.attempts[user_id].append(current_time)
        
        self.attempts[user_id] = [
            t for t in self.attempts[user_id]
            if current_time - t < timedelta(seconds=300)
        ]

    def is_locked_out(self, user_id):
        if user_id not in self.lockouts:
            return False
        
        lockout_time = self.lockouts[user_id]
        if datetime.now() - lockout_time > timedelta(seconds=self.lockout_duration):
            del self.lockouts[user_id]
            self.attempts[user_id] = []
            return False
        
        return True

    def check_brute_force(self, user_id):
        if len(self.attempts[user_id]) >= self.max_attempts:
            self.lockouts[user_id] = datetime.now()
            return True
        
        return False

    def get_attempt_count(self, user_id):
        current_time = datetime.now()
        self.attempts[user_id] = [
            t for t in self.attempts[user_id]
            if current_time - t < timedelta(seconds=300)
        ]
        return len(self.attempts[user_id])

    def reset_attempts(self, user_id):
        if user_id in self.attempts:
            self.attempts[user_id] = []
        if user_id in self.lockouts:
            del self.lockouts[user_id]
