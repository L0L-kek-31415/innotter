from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "moderator"


class IsModerOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return IsModer.has_permission(
            self, request, view
        ) or permissions.IsAdminUser.has_permission(self, request, view)


class IsOwnerOrModerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return IsOwner.has_permission(
            self, request, view
        ) or IsOwnerOrModerOrAdmin.has_permission(self, request, view)


class IsBlocked(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_blocked is False
