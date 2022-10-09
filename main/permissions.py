from rest_framework import permissions
from django.utils import timezone


class IsPageBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.unblock_date:
            if obj.unblock_date >= timezone.now():
                return False
        return True


class IsPagePrivate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.isPprivate is False
