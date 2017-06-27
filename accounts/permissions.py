from django.utils.translation import ugettext_lazy as _

from rest_framework import permissions, exceptions

from .models import User


class IsAdvertiser(permissions.IsAuthenticated):
    """
    permission for user advertiser role
    """

    def has_permission(self, request, view):
        # import pdb;pdb.set_trace()
        if request.user.role == User.ADVERTISER:
            return True


class IsAdvertiserOrReadOnly(permissions.IsAuthenticated):
    """
    permission for user advertiser role
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.role == User.ADVERTISER:
                return True


class IsAdmin(permissions.IsAuthenticated):
    """
    permission for user admin role
    """

    def has_permission(self, request, view):
        if request.user.role == User.ADMIN:
            return True


class IsAdminOrReadOnly(permissions.IsAuthenticated):
    """
    permission for user admin role
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated() and request.user.role == User.ADMIN:
                return True


class IsRegisterAdvertiserOrLoginAdvertiser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated() and request.user.role == User.ADVERTISER:
            return True
        else:
            user_id = request.data.get('user')
            try:
                user = User.objects.get(id=user_id)
                if not user.is_active:
                    request.user=user
                    return True
                else:
                    return False
            except:
                return False



class IsInactiveUserOrLoginUser(permissions.BasePermission):

    def has_permission(self, request, view):
        user_id = request.data.get('user')
        if (not user_id) and request.user.is_authenticated():
            return True
        else:
            try:
                user = User.objects.get(id=user_id)
                if not user.is_active:
                    request.user=user
                    return True
                else:
                    return False
            except:
                return False


class IsAdminOrAdvertiser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == User.ADMIN or request.user.role == User.ADVERTISER:
            return True