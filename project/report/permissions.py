from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            if request.data.get('user', '') == str(request.user.id):
                return True
            elif request.user.is_staff:
                return True
            else:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission to only allow owners/admin of an object to access/edit it.
        """
        if request.method in ['HEAD', 'OPTIONS']:
            return True

        # print(f'obj.user: {obj.user} ; request.user: {request.user}')

        return obj.user == request.user or request.user.is_staff
