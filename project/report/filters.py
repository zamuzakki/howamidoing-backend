from django_filters import filters, FilterSet
from project.report.models.status import Status
from project.report.models.report import Report


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
