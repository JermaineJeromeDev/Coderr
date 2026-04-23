"""
Central permission logic for the Coderr platform.
"""

from rest_framework import permissions
from django.contrib.auth import get_user_model


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows write access only to the owner of the object.
    Supports fields: user, reviewer, customer_user.
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks ownership based on the object type or specific owner fields.
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, get_user_model()):
            return obj == request.user

        owner_field = getattr(
            obj, 'user',
            getattr(obj, 'reviewer', getattr(obj, 'customer_user', None))
        )

        return owner_field == request.user