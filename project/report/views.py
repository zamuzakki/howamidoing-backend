from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_gis.filters import TMSTileFilter, InBBoxFilter
from .models.status import Status
from .models.report import Report
from .models.km_grid import KmGrid
from .models.km_grid_score import KmGridScore
from .models.user import User
from .filters import KmGridFilter, KmGridScoreFilter, ReportFilter
from .serializers import StatusSerializer, ReportSerializer, ReportCreateSerializer,\
    ReportRetrieveListSerializer, UserSerializer, KmGridSerializer,\
    KmGridScoreSerializer
import json


class StatusViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    retrieve:
        Show Report object details.
        <br>
        Parameter <strong>id</strong> is the ID of the report that you want to see.

    list:
        Show list of Report object.
        <br>
        Parameter <strong>page</strong> indicates the page number.
        Each page consists of 100 objects
    """

    serializer_class = StatusSerializer
    queryset = Status.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)


class ReportViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
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
    """

    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ReportFilter

    def create(self, request, *args, **kwargs):
        try:
            grid = KmGrid.objects.geometry_contains(
                json.dumps(request.data['location'])
            )
            if grid.count() > 0:
                request.data['grid'] = grid.first().id

            print(request.data)

            serializer = ReportSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            print(e)
            return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        mixins.CreateModelMixin.perform_create(self, serializer)
        headers = mixins.CreateModelMixin.get_success_headers(self, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        """
        Get permission object for certain action
        :return: Permission object
        """
        permission_classes = [AllowAny]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Get serializer class for certain action
        :return: Serializer class
        """
        serializer_class = ReportSerializer
        if self.action == 'create':
            serializer_class = ReportCreateSerializer
        if self.action in ['retrieve', 'list']:
            serializer_class = ReportRetrieveListSerializer
        return serializer_class


class KmGridViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
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
    """

    serializer_class = KmGridSerializer
    queryset = KmGrid.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = KmGridFilter


class KmGridScoreViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    """
    retrieve:
        Show KmGridScore object details.
        <br>
        Parameter <strong>id</strong> is the ID of the KM grid_score that you want to see.

    list:
        Show list of KmGridScore object.
        <br>
        Parameter <strong>page</strong> indicates the page number.
        Each page consists of 100 objects
    """

    serializer_class = KmGridScoreSerializer
    queryset = KmGridScore.objects.all()
    filter_backends = (filters.DjangoFilterBackend, InBBoxFilter, TMSTileFilter)
    filterset_class = KmGridScoreFilter


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  viewsets.GenericViewSet):
    """
    retrieve:
        Show User object details.
        <br>
        Parameter <strong>id</strong> is the ID of the User that you want to see.

    retrieve:
        List User object.
        <br>

    create:
        Create new User.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Get permission object for certain action
        :return: Permission object
        """
        permission_classes = [AllowAny]
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
