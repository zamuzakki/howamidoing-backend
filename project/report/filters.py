from rest_framework_gis.filterset import GeoFilterSet
from rest_framework_gis.filters import GeometryFilter
from django_filters import filters
from .models import KmGrid


class KmGridFilter(GeoFilterSet):
    max_population = filters.NumberFilter(field_name='population', lookup_expr='lte')
    min_population = filters.NumberFilter(field_name='population', lookup_expr='gte')
    contains_geom = GeometryFilter(field_name='geometry', lookup_expr='contains')

    class Meta:
        model = KmGrid
        fields = ['max_population', 'min_population', 'contains_geom']
