from .models import Report, Status
from django.utils import timezone


def auto_revert_status_to_all_well_here():
    last_report_qs = Report.objects.all().order_by('user', '-id').distinct('user')
    for report in last_report_qs:
        if (report.timestamp - timezone.now()).days >= 3:
            try:
                new_report = Report.objects.create(
                    location=report.location,
                    user=report.user,
                    status=Status.objects.get(name_icontains='well')
                )
            except Exception as e:
                print(e)
                new_report = Report.objects.create(
                    location=report.location,
                    user=report.user,
                    status=None
                )

            new_report.save()
