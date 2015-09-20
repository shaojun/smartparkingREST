from rest_framework import permissions
#from django.contrib.auth.models import User

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
            return obj.owner == request.user

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

class IsOwnerThenReadOnlyOrDeny(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.owner == request.user

class IsOwnerOrDeny(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user:
            if request.user.groups.filter(name='SuperUsers').exists():
                return True
        return obj.owner == request.user

class IsUserInfoSelfOrDeny(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='SuperUsers').exists():
            return True
        return obj.user == request.user

class IsUserSelfOrDeny(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='SuperUsers').exists():
            return True
        return obj == request.user

class IsSuperUsersGroupOrDeny(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='SuperUsers').exists():
            return True
        return False

class IsSuperUsersGroupOrPostOnly(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     return obj == request.user

    def has_permission(self, request, view):
        if request.user.is_anonymous():
            if request.method in permissions.SAFE_METHODS:
                return False
            else:
                return True
        if request.user.groups.filter(name='SuperUsers').exists():
            return True
        return False

class IsSuperUsersGroupThenListOrUserSelfThenReturnSelfInfoOrPostOnly(permissions.BasePermission):
    # def has_object_permission(self, request, view, obj):
    #     return obj == request.user

    def has_permission(self, request, view):
        if request.user.is_anonymous():
            if request.method in permissions.SAFE_METHODS:
                return False
            else:
                return True
        if request.user.groups.filter(name='SuperUsers').exists():
            return True
        return False

class IsRobotsGroupOrDeny(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user:
            if request.user.groups.filter(name='Robots').exists() or request.user.groups.filter(name='SuperUsers').exists():
                return True
        return False

class IsRobotsGroupOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user:
            if request.user.groups.filter(name='Robots').exists() or request.user.groups.filter(name='SuperUsers').exists():
                return True
        if request.method in permissions.SAFE_METHODS:
            # if request.user.groups.filter(name='Technicians').exists():
            return True
        return False

class IsTechniciansGroupOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_permission(self, request, view):
        if request.user:
            if request.user.groups.filter(name='Technicians').exists() or request.user.groups.filter(name='SuperUsers').exists():
                return True
        if request.method in permissions.SAFE_METHODS:
            # if request.user.groups.filter(name='Technicians').exists():
            return True
        return False
