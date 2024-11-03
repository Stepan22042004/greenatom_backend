from rest_framework.permissions import BasePermission


class IsEmployeeOrAdmin(BasePermission):
    def has_permission(self, request, view):
        pk = view.kwargs.get('pk')
        if request.user and (request.user.organisations.filter(pk=pk).exists()
           or request.user.is_staff):
            return True
        return False
