from django.contrib.gis.geos import fromstr
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from .user import User
from .km_grid import KmGrid
from .status import Status
import logging

logger = logging.getLogger(__name__)


class ReportQuerySet(models.QuerySet):
    """Custom QuerySet for Report."""

    def location_within(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=4326)
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
        geometry = fromstr(geojson_geometry_string, srid=4326)
        return self.get_queryset().filter(
            location__within=geometry
        )

    def status_contains(self, status_name):
        return self.get_queryset().filter(
            status__name__icontains=status_name
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

    objects = models.Manager()
    current_objects = ReportManager()

    def __str__(self):
        if self.grid:
            return '{} | {} | {} | {}'.format(self.id, self.grid.id, self.timestamp, self.user.id)
        else:
            return '{} | {} | {}'.format(self.id, self.timestamp, self.user.id)

    class Meta:
        ordering = ('-id',)


@receiver(pre_save, sender=Report)
def mark_old_report(sender, instance, **kwargs):
    """
    Set False to previous status `current` field
    """
    Report.objects.filter(user=instance.user).update(current=False)
