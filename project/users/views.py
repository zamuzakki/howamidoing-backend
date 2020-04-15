from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Show User object details.
        <br>
        Parameter <strong>id</strong> is the ID of the User that you want to see.

    list:
        Show list of User object.
        <br>
        Parameter <strong>page</strong> indicates the page number.
        Each page consists of 100 objects

    create:
        Create new User.

    destroy:
        Delete User object.
        <br>
        Parameter <strong>id</strong> is the ID of the User that you want to delete.

    update:
        Update User object.
        <br>
        Parameter <strong>id</strong> is the ID of the User that you want to update.

    partial_update:
        Update User object.
        <br>
        Parameter <strong>id</strong> is the ID of the User that you want to update.
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Get serializer class for certain action
        :return: Serializer class
        """
        serializer_class = UserSerializer
        if self.action == 'create':
            serializer_class = CreateUserSerializer
        return serializer_class

    def get_permissions(self):
        """
        Get permission object for certain action
        :return: Permission object
        """
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        if self.action == 'list' or self.action == 'partial_update' or \
                self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsUserOrReadOnly]
        return [permission() for permission in permission_classes]
