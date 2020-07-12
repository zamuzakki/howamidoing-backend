from django.contrib.gis.geos import fromstr
from django.contrib.gis.db import models as gis
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from .user import User
from .km_grid import KmGrid
from .km_grid_score import KmGridScore
from .status import Status
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
def report_pre_save_signal(sender, instance, **kwargs):
    """
    Set False to previous status `current` field
    """
    Report.objects.filter(user=instance.user).update(current=False)

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
        grid_score, created = KmGridScore.objects.get_or_create(geometry=instance.grid.geometry)

        # if grid is just created, then set its attribute
        if created:
            grid_score.population = instance.grid.population
            grid_score.total_report += 1
            grid_score.set_color_score_by_status(instance.status)
            grid_score.set_color_count_by_status(instance.status)
        else:
            # if grid exists, check if the instance is the first report created by
            # the user in that grid
            user_report = Report.objects.filter(user=instance.user, grid=instance.grid)

            # If yes, update grid attributes
            if user_report.count() == 1:
                grid_score.total_report += 1
                grid_score.set_color_score_by_status(instance.status)
                grid_score.set_color_count_by_status(instance.status)

            # If no, check if current report has the same status as the previous one
            else:
                prev_report = user_report[1]

                # If yes, we decrement the old status count in the grid and recalculate that status score
                # Then increment the newstatus count in the grid and recalculate that status score
                if not instance.status == prev_report.status:
                    grid_score.set_color_score_by_status(prev_report.status)
                    grid_score.set_color_count_by_status(prev_report.status, 'sub')

                    grid_score.set_color_score_by_status(instance.status)
                    grid_score.set_color_count_by_status(instance.status)
