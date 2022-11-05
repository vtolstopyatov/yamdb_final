from rest_framework import permissions


class ModerateAccessOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )


class AdminAccessOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser
            or request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return (
                request.user.is_superuser
                or request.user.is_admin
            )
        return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
