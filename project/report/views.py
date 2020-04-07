from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Status, Report
from .serializers import StatusSerializer, ReportSerializer


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

    permission_classes = (IsAuthenticated,)
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


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

    permission_classes = (IsAuthenticated,)
    serializer_class = ReportSerializer
    queryset = Report.objects.all()