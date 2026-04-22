from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner_field = getattr(obj, 'user', 
                    getattr(obj, 'reviewer', 
                    getattr(obj, 'customer_user', None)))
        return owner_field == request.user