from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Status, Report, KmGrid
from .permissions import IsAdminOrOwner
from .filters import KmGridFilter
from .serializers import StatusSerializer, ReportSerializer, \
    ReportCreateUpdateSerializer, KmGridSerializer


class StatusViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Show Status object details.
        <br>
        Parameter <strong>id</strong> is the ID of the status that you want to see.

    list:
        Show list of Status object.
        <br>
        Parameter <strong>page</strong> indicates the page number.
        Each page consists of 100 objects

    create:
        Create new Status.

    destroy:
        Delete Status object.
        <br>
        Parameter <strong>id</strong> is the ID of the status that you want to delete.

    update:
        Update Status object.
        <br>
        Parameter <strong>id</strong> is the ID of the status that you want to update.

    partial_update:
        Update Status object.
        <br>
        Parameter <strong>id</strong> is the ID of the status that you want to update.
    """

    serializer_class = StatusSerializer
    queryset = Status.objects.all()

    def get_permissions(self):
        """
        Get permission object for certain action
        :return: Permission object
        """
        permission_classes = []
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or \
                self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ReportViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Show Report object details.
        <br>
        Parameter <strong>id</strong> is the ID of the Report that you want to see.

    list:
        Show list of Report object.
        <br>
        Parameter <strong>page</strong> indicates the page number.
        Each page consists of 100 objects

    create:
        Create new Report.

    destroy:
        Delete Report object.
        <br>
        Parameter <strong>id</strong> is the ID of the Report that you want to delete.

    update:
        Update Report object.
        <br>
        Parameter <strong>id</strong> is the ID of the Report that you want to update.

    partial_update:
        Update Report object.
        <br>
        Parameter <strong>id</strong> is the ID of the Report that you want to update.
    """

    queryset = Report.objects.all()

    def get_permissions(self):
        """
        Get permission object for certain action
        :return: Permission object
        """
        permission_classes = []
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or \
                self.action == 'retrieve':
            permission_classes = [IsAdminOrOwner]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Get serializer class for certain action
        :return: Serializer class
        """
        serializer_class = ReportSerializer
        if self.action == 'create' or self.action == 'update':
            serializer_class = ReportCreateUpdateSerializer
        return serializer_class


class KmGridViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Show KmGrid object details.
        <br>
        Parameter <strong>id</strong> is the ID of the KM grid that you want to see.

    list:
        Show list of KmGrid object.
        <br>
        Parameter <strong>page</strong> indicates the page number.
        Each page consists of 100 objects

    create:
        Create new KmGrid.

    destroy:
        Delete KmGrid object.
        <br>
        Parameter <strong>id</strong> is the ID of the KM grid that you want to delete.

    update:
        Update KmGrid object.
        <br>
        Parameter <strong>id</strong> is the ID of the KM grid that you want to update.

    partial_update:
        Update KmGrid object.
        <br>
        Parameter <strong>id</strong> is the ID of the KM grid that you want to update.
    """

    serializer_class = KmGridSerializer
    queryset = KmGrid.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = KmGridFilter

    def get_permissions(self):
        """
        Get permission object for certain action
        :return: Permission object
        """
        permission_classes = []
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update' or \
                self.action == 'destroy':
            permission_classes = [IsAdminUser]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
