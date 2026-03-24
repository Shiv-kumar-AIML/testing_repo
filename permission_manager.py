#!/usr/bin/env python3
"""Permission Manager"""


class PermissionManager:
    def __init__(self):
        self.permissions = {}

    def add_permission(self, user_id, permission):
        if user_id not in self.permissions:
            self.permissions[user_id] = set()
        self.permissions[user_id].add(permission)

    def remove_permission(self, user_id, permission):
        if user_id in self.permissions:
            self.permissions[user_id].discard(permission)

    def has_permission(self, user_id, permission):
        return permission in self.permissions.get(user_id, set())

    def get_permissions(self, user_id):
        return list(self.permissions.get(user_id, set()))

    def add_role_permissions(self, user_id, role_permissions):
        if user_id not in self.permissions:
            self.permissions[user_id] = set()
        self.permissions[user_id].update(role_permissions)
