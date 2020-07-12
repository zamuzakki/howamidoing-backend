from django.contrib.gis.geos import fromstr
from django.contrib.gis.db import models as gis
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from .user import User
from .report_point_score import ReportPointScore
from .km_grid import KmGrid
from .status import Status
import logging

logger = logging.getLogger(__name__)


class ReportPointQuerySet(models.QuerySet):
    """Custom QuerySet for ReportPoint."""

    def location_within(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=3857)
        return self.filter(
            location__within=geometry
        )

    def status_contains(self, status_name):
        return self.filter(
            status__name__icontains=status_name
        )

    def green_report(self):
        return self.status_contains('well')

    def yellow_report(self):
        return self.status_contains('food')

    def red_report(self):
        return self.status_contains('medic')


class ReportPointManager(models.Manager):
    """Custom Manager for ReportPoint."""

    def get_queryset(self):
        return ReportPointQuerySet(self.model, using=self._db)

    def location_within(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=3857)
        return self.get_queryset().filter(
            location__within=geometry
        )

    def green_report(self):
        return self.get_queryset().status_contains('well')

    def yellow_report(self):
        return self.get_queryset().status_contains('food')

    def red_report(self):
        return self.get_queryset().status_contains('medic')


class CurrentReportPointManager(ReportPointManager):
    """Custom Manager for ReportPoint."""

    def get_queryset(self):
        return ReportPointQuerySet(self.model, using=self._db).filter(
            current=True
        )


class ReportPoint(models.Model):
    """
    Report about latest user status.
    Everytime user renew their status, system will create a new ReportPoint instead of updating the old one.
    """

    status = models.ForeignKey(
        Status,
        help_text=_('Status of this report'),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    timestamp = models.DateTimeField(
        help_text=_('Timestamp of report creation'),
        auto_now_add=True
    )

    user = models.ForeignKey(
        User,
        help_text=_('Owner/user of this report'),
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    current = models.BooleanField(
        help_text=_('Flag to indicate current status.'),
        default=True
    )

    location = gis.PointField(
        help_text=_('Location of the user when making the Report.'),
        srid=3857
    )

    grid = models.ForeignKey(
        KmGrid,
        help_text=_('Grid reference of the report'),
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE
    )

    objects = models.Manager()
    current_objects = ReportPointManager()

    def __str__(self):
        if self.grid:
            return '{} | {} | {} | {}'.format(self.id, self.grid.id, self.timestamp, self.user.id)
        else:
            return '{} | {} | {}'.format(self.id, self.timestamp, self.user.id)

    class Meta:
        ordering = ('-id',)


@receiver(pre_save, sender=ReportPoint)
def report_point_pre_save_signal(sender, instance, **kwargs):
    """
    Set False to previous status `current` field
    """
    ReportPoint.objects.filter(user=instance.user).update(current=False)

@receiver(post_save, sender=ReportPoint)
def report_point_post_save_signal(sender, instance, created, **kwargs):
    """
    This is the post save signal for post ReportPoint creation
    assuming current report's location is just the same with previous one.
    It's quarantine afterall.
    :param instance: Report instance
    """

    # Only do when grid is not None
    report_point_score, created = ReportPointScore.objects.get_or_create(location=instance.location)

    # if report_point_score is just created, then set its attribute
    if created:
        report_point_score.population = instance.grid.population
        report_point_score.total_report += 1
        report_point_score.set_color_score_by_status(instance.status)
        report_point_score.set_color_count_by_status(instance.status)
    else:
        # if report_point_score exists, check if the instance is the first report created by
        # the user in that area
        user_report = ReportPoint.objects.filter(user=instance.user, location=instance.grid)

        # If yes, update grid attributes
        if user_report.count() == 1:
            report_point_score.total_report += 1
            report_point_score.set_color_score_by_status(instance.status)
            report_point_score.set_color_count_by_status(instance.status)

        # If no, check if current report has the same status as the previous one
        else:
            prev_report = user_report[1]

            # If yes, we decrement the old status count in the grid and recalculate that status score
            # Then increment the newstatus count in the grid and recalculate that status score
            if not instance.status == prev_report.status:
                report_point_score.set_color_score_by_status(prev_report.status)
                report_point_score.set_color_count_by_status(prev_report.status, 'sub')

                report_point_score.set_color_score_by_status(instance.status)
                report_point_score.set_color_count_by_status(instance.status)
