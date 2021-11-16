"""Managing permission."""
from rest_framework import permissions

from client.models import Client
from proprietaire.models import Proprietaire
from societe.models import RealEstate


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    """Is logged in user or admin."""

    def has_object_permission(self, request, view, obj):
        """Is logged in user or admin permission."""
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    """Is adminuser."""

    def has_permission(self, request, view):
        """Statff."""
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        """Staff."""
        return request.user and request.user.is_staff


class IsLessor(permissions.BasePermission):
    """Is Lessor."""

    def has_permission(self, request, view):
        """Check if user is lessor."""
        if request.user.is_anonymous:
            return False
        lessor = Proprietaire.objects.filter(user__id=request.user.id).exists()
        return request.user and lessor

    def has_object_permission(self, request, view, obj):
        """lessor."""
        if request.user.is_anonymous:
            return False
        return obj.created_by == request.user


class IsTenant(permissions.BasePermission):
    """Is client."""

    def has_permission(self, request, view):
        """Check if user is a client."""
        if request.user.is_anonymous:
            return False
        client = Client.objects.filter(user__id=request.user.id).exists()
        return request.user and client

    def has_object_permission(self, request, view, obj):
        """lessor."""
        if request.user.is_anonymous:
            return False
        return obj.created_by == request.user

class IsRealEstate(permissions.BasePermission):
    """Is Real estate."""

    def has_permission(self, request, view):
        """Check if user is a real estate owner."""
        if request.user.is_anonymous:
            return False
        real_estate = RealEstate.objects.filter(created_by=request.user).exists()
        return real_estate

    def has_object_permission(self, request, view, obj):
        """real estate."""
        if request.user.is_anonymous:
            return False
        return obj.created_by == request.user
