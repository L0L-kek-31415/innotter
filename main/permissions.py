from rest_framework import permissions
from django.utils import timezone

from main.models import Page


class IsPageNotBlocked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.unblock_date:
            if obj.unblock_date >= timezone.now():
                return False
        return True


class IsPageNotPrivate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_private is False


class IsPageOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Page):
            return obj.owner == request.user
        return True
