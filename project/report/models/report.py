from django.contrib.gis.geos import fromstr
from django.core import management
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from project.report.models.user import User
from project.report.models.km_grid import KmGrid
from project.report.models.status import Status
import logging

logger = logging.getLogger(__name__)


class ReportQuerySet(models.QuerySet):
    """Custom QuerySet for Report."""

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


class ReportManager(models.Manager):
    """Custom Manager for Report."""

    def get_queryset(self):
        return ReportQuerySet(self.model, using=self._db)

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


class CurrentReportManager(ReportManager):
    """Custom Manager for Report."""

    def get_queryset(self):
        return ReportQuerySet(self.model, using=self._db).filter(
            current=True
        )


class Report(models.Model):
    """
    Report about latest user status.
    Everytime user renew their status, system will create a new Report instead of updating the old one.
    """
    grid = models.ForeignKey(
        KmGrid,
        help_text=_('Grid reference of the report'),
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE
    )

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

    objects = ReportManager()

    def __str__(self):
        if self.grid:
            return '{} | {} | {} | {} | {}'.format(
                self.id, self.current, self.status.id, self.grid.id, self.user.id
            )
        else:
            return '{} | {} | {} | {}'.format(self.id, self.current, self.status.id, self.user.id)

    class Meta:
        ordering = ('-id',)


@receiver(pre_save, sender=Report)
def report_pre_save_signal(sender, instance, **kwargs):
    """
    Set False to previous status `current` field
    """
    try:
        Report.objects.filter(user=instance.user).update(current=False)
    except Report.DoesNotExist:
        pass

@receiver(post_save, sender=Report)
def report_post_save_signal(sender, instance, created, **kwargs):
    """
    This is the post save signal for post creation.
    KmGridScore assuming current report's grid
    is just the same with previous one. It's quarantine afterall.
    :param instance: Report instance
    """

    # Only do when grid is not None
    if instance.grid is not None:
        # check previous report. If it has different grid, recalculate both grid.
        # If grid is the same, only recalculate score for that grid.
        try:
            prev_report = Report.objects.filter(user=instance.user, current=False).latest('id')
        except Report.DoesNotExist:
            prev_report = None
        if prev_report:
            if prev_report.grid == instance.grid:
                management.call_command(
                    'generate_grid_score',
                    '--grids={}'.format(instance.grid.id)
                )
            else:
                management.call_command(
                    'generate_grid_score',
                    '--grids={},{}'.format(instance.grid.id, prev_report.grid.id)
                )
        else:
            management.call_command(
                'generate_grid_score',
                '--grids={}'.format(instance.grid.id)
            )
