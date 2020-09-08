from django_filters import rest_framework as filters
from django.contrib.gis.gdal import gdal_version
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import viewsets, mixins, status
from rest_framework.serializers import ValidationError
from rest_framework_mvt.views import BaseMVTView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework_gis.filters import TMSTileFilter
from project.report.models.status import Status
from project.report.models.report import Report
from project.report.models.km_grid import KmGrid
from project.report.models.user import User
from project.report.utils.common_function import flip_geojson_coordinates
from project.report.filters import ReportFilter, StatusFilter
from project.report.serializers import StatusSerializer, ReportSerializer, ReportCreateSerializer,\
    ReportRetrieveListSerializer, UserSerializer
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
    filterset_class = StatusFilter


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
                request.data['location']
            )
            if grid.count() > 0:
                request.data['grid'] = grid.first().id

            serializer = ReportSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception:
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


class UserViewSet(mixins.ListModelMixin,
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


class KmGridScoreMVTView(BaseMVTView):
    # pylint: disable=unused-argument
    def get(self, request, *args, **kwargs):
        params = request.GET.dict()
        if params.pop("tile", None) is not None:
            try:
                limit, offset = self._validate_paginate(
                    params.pop("limit", None), params.pop("offset", None)
                )
            except ValidationError:
                limit, offset = None, None

            bbox = TMSTileFilter().get_filter_bbox(request)
            if gdal_version().decode("utf-8").split('.')[0] == '3':
                bbox_geojson = json.loads(bbox.geojson)
                flip_geojson_coordinates(bbox_geojson)
                bbox_geojson = json.dumps(bbox_geojson)

            try:
                bbox = GEOSGeometry(bbox_geojson, srid=4326)
                bbox.transform(3857)
            except Exception:
                print('Error Transforming or creating Geometry')

            try:
                mvt = self.model.vector_tiles.intersect(
                    bbox=bbox, limit=limit, offset=offset, filters=params
                )
                status = 200 if mvt else 204
            except Exception:
                mvt = b""
                status = 400
        else:
            mvt = b""
            status = 400

        return Response(
            bytes(mvt), content_type="application/vnd.mapbox-vector-tile", status=status
        )


def mvt_view_factory(model_class, geom_col="geom"):
    return type(
        f"{model_class.__name__}MVTView",
        (KmGridScoreMVTView,),
        {"model": model_class, "geom_col": geom_col},
    ).as_view()
