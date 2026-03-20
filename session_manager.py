#!/usr/bin/env python3
"""Session Manager"""

import uuid
from datetime import datetime, timedelta


class Session:
    def __init__(self, user_id, timeout_minutes=30):
        self.user_id = user_id
        self.session_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.timeout = timedelta(minutes=timeout_minutes)

    def is_expired(self):
        return datetime.now() - self.created_at > self.timeout

    def get_info(self):
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "expired": self.is_expired()
        }
