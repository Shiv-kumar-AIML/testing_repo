#!/usr/bin/env python3
"""Rate Limiter for Security Testing"""


class RateLimiter:
    def __init__(self, max_attempts=5, time_window=60):
        self.max_attempts = max_attempts
        self.time_window = time_window
        self.attempts = {}

    def is_allowed(self, user_id):
        import time
        current_time = time.time()
        
        if user_id not in self.attempts:
            self.attempts[user_id] = []
        
        self.attempts[user_id] = [
            t for t in self.attempts[user_id] 
            if current_time - t < self.time_window
        ]
        
        if len(self.attempts[user_id]) < self.max_attempts:
            self.attempts[user_id].append(current_time)
            return True
        return False

    def get_remaining(self, user_id):
        if user_id not in self.attempts:
            return self.max_attempts
        return self.max_attempts - len(self.attempts[user_id])


if __name__ == "__main__":
    limiter = RateLimiter(max_attempts=3, time_window=10)
    
    for i in range(5):
        user_id = "user1"
        allowed = limiter.is_allowed(user_id)
        remaining = limiter.get_remaining(user_id)
        print(f"Attempt {i+1}: Allowed={allowed}, Remaining={remaining}")
