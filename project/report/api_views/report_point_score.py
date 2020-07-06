from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_gis.filters import InBBoxFilter
from project.report.models.report_point_score import ReportPointScore
from project.report.filters import ReportPointScoreFilter
from project.report.serializers import ReportPointScoreSerializer


class ReportPointScoreViewSet(mixins.RetrieveModelMixin,
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

    serializer_class = ReportPointScoreSerializer
    bbox_filter_field = 'location'
    queryset = ReportPointScore.objects.all()
    filter_backends = (filters.DjangoFilterBackend, InBBoxFilter)
    filterset_class = ReportPointScoreFilter

    def list(self, request, *args, **kwargs):
        if 'no_page' in request.query_params:
            self.pagination_class = None
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)