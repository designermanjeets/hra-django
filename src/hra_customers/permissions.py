from rest_framework import permissions

class IsTenantUser(permissions.BasePermission):
    """
    Custom permission to only allow users of a tenant to access the resource.
    """

    def has_permission(self, request, view):
        # Implement your custom permission logic here
        # For example, check if the user is part of the tenant
        return request.user and request.user.is_authenticated and request.user.tenant_id is not None