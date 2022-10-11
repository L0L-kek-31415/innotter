from rest_framework import permissions
from django.utils import timezone


class IsPageNotBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.unblock_date:
            if obj.unblock_date >= timezone.now():
                return False
        return True


class IsPageNotPrivate(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.is_private is False
