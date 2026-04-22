from rest_framework import permissions
from django.contrib.auth import get_user_model

User = get_user_model()

class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, get_user_model()):
            return obj == request.user
        owner_field = getattr(obj, 'user', 
                    getattr(obj, 'reviewer', 
                    getattr(obj, 'customer_user', None)))
        return owner_field == request.user