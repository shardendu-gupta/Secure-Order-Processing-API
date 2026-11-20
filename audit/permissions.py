from rest_framework.permissions import BasePermission



class AuditPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (request.user.is_superuser or request.user.role in ['ADMIN', 'STAFF'])


