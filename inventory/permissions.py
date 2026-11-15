from rest_framework.permissions import BasePermission, SAFE_METHODS



class InventoryPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authneticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return (request.user.is_superuser  or request.user.role in ['ADMIN', 'STAFF'])


class InventoryHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (request.user.is_superuser or request.user.role in ['ADMIN', 'STAFF'])

