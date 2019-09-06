"""Managing permission."""
from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    """Is logged in user or admin."""

    def has_object_permission(self, request, view, obj):
        """Is logges in user or admin permission."""
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    """Is adminuser."""

    def has_permission(self, request, view):
        """Statff."""
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """Staff."""
        return request.user and request.user.is_staff
