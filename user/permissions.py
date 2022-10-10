from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "moderator"


class IsBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_blocked is False
