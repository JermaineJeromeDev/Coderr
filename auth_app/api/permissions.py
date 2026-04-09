from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Erlaubt GET für jeden Authentifizierten, 
    aber PATCH/PUT nur für den Besitzer.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
