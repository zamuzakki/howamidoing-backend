from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters
from .models import KmGrid, KmGridScore


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
