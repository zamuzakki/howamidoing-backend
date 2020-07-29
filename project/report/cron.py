from .models import Report, Status
from django.utils import timezone
from .management.commands.generate_grid_score import generate_grid_score

def auto_revert_status_to_all_well_here():
    """
    Auto revert user status to 'All Well Here' if there is no update for 3 days
    """
    last_report_qs = Report.objects.all().order_by('user', '-id').distinct(
        'user'
    ).select_related('status')
    for report in last_report_qs:
        if (report.timestamp - timezone.now()).days >= 3 and 'well' not in report.status.name.lower():
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

def auto_generate_grid_score():
    """
    Automatically generate KmGridScore every night
    """
    generate_grid_score(select='all')
