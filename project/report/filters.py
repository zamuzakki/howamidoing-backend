from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters, FilterSet
from .models.status import Status
from .models.report import Report
from .models.report_point import ReportPoint
from .models.report_point_score import ReportPointScore
from .models.km_grid import KmGrid
from .models.km_grid_score import KmGridScore


class StatusFilter(FilterSet):
    name_contains = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Status
        fields = ['name_contains']


class ReportFilter(FilterSet):
    current = filters.BooleanFilter(field_name='current')
    user = filters.CharFilter(field_name='user')

    class Meta:
        model = Report
        fields = ['current']


class ReportPointFilter(FilterSet):
    current = filters.BooleanFilter(field_name='current')
    user = filters.CharFilter(field_name='user')

    class Meta:
        model = ReportPoint
        fields = ['current']


class ReportPointScoreFilter(FilterSet):
    total_score = filters.NumberFilter(field_name='total_score')
    min_total_report = filters.NumberFilter(field_name='total_report', lookup_expr='gte')
    max_total_report = filters.NumberFilter(field_name='total_report', lookup_expr='lte')
    contains_geom = GeometryFilter(field_name='location', lookup_expr='contains')

    class Meta:
        model = ReportPointScore
        fields = ['total_score', 'min_total_report', 'max_total_report', 'contains_geom']


class KmGridFilter(GeoFilterSet):
    max_population = filters.NumberFilter(field_name='population', lookup_expr='lte')
    min_population = filters.NumberFilter(field_name='population', lookup_expr='gte')
    contains_geom = GeometryFilter(field_name='geometry', lookup_expr='contains')

    class Meta:
        model = KmGrid
        fields = ['max_population', 'min_population', 'contains_geom']


class KmGridScoreFilter(KmGridFilter):
    total_score = filters.NumberFilter(field_name='total_score')
    min_total_report = filters.NumberFilter(field_name='total_report', lookup_expr='gte')
    max_total_report = filters.NumberFilter(field_name='total_report', lookup_expr='lte')

    class Meta:
        model = KmGridScore
        fields = KmGridFilter.Meta.fields + ['total_score', 'min_total_report', 'max_total_report']
