from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser, AllowAny
from project.report.models.report_point import ReportPoint
from project.report.filters import ReportPointFilter
from project.report.serializers import ReportPointSerializer

class ReportPointViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """
    retrieve:
        Show ReportPoint object details.
        <br>
        Parameter <strong>id</strong> is the ID of the ReportPoint that you want to see.

    list:
        Show list of ReportPoint object.
        <br>
        Parameter <strong>page</strong> indicates the page number.
        Each page consists of 100 objects

    create:
        Create new ReportPoint.

    destroy:
        Delete ReportPoint object.
        <br>
        Parameter <strong>id</strong> is the ID of the ReportPoint that you want to delete.
    """

    serializer_class = ReportPointSerializer
    queryset = ReportPoint.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ReportPointFilter

    def get_permissions(self):
        """
        Get permission object for certain action
        :return: Permission object
        """
        permission_classes = [AllowAny]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


