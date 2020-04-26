from django.contrib.gis.db import models as gis
from django.db import models
from project.users.models import User
from django.utils.translation import ugettext_lazy as _
from .utils.scoring_grid import color_score_km_grid, status_score_km_grid
import logging

logger = logging.getLogger(__name__)


class Status(models.Model):
    """
    Status used in report, e.g. 'All Well Here', 'We Need Medical Help', etc.
    """
    name = models.CharField(
        help_text=_('Name of this status'),
        max_length=50,
        null=False,
        blank=False,
        default=''
    )

    description = models.TextField(
        help_text=_('Brief description of this status'),
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return '{} | {}'.format(self.id, self.name)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Statuses'


class Report(models.Model):
    """
    Report about latest user status.
    Everytime user renew their status, system will create a new Report instead of updating the old one.
    """
    location = gis.PointField(
        help_text=_('Location of the report/user Location'),
        null=True,
        default=None,
        blank=True
    )

    status = models.ForeignKey(
        Status,
        help_text=_('Status of this report'),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        default=1
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
        blank=False,
        default=1
    )

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.id, self.location, self.timestamp, self.user.username)

    class Meta:
        ordering = ('-id',)


class KmGrid(models.Model):
    """
    Model representing grid and its population number.
    Data will be generated using Positgis and Worldpop.
    """
    geometry = gis.PolygonField(
        help_text=_('Geometry of this grid'),
        null=True,
        blank=True,
        default=None
    )

    population = models.IntegerField(
        help_text=_('Number of people in this grid'),
        null=False,
        blank=False,
        default=300
    )

    def __str__(self):
        return '{} | {} | {}'.format(self.id, self.geometry, self.population)

    class Meta:
        # Temporarily set managed to False because we still don't know
        # how to create the data
        managed = False
        ordering = ('-id',)


class KmGridScore(models.Model):
    """
    Materialized uiews for user status summary per grid
    """
    geometry = gis.PolygonField(
        help_text=_('Geometry of this Grid'),
        null=True,
        blank=True,
        default=None
    )

    score_green = models.DecimalField(
        help_text=_('The score of user with latest "All is Well" status in this grid'),
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )

    count_green = models.SmallIntegerField(
        help_text=_('The number of user with latest "All is Well" status in this grid'),
        null=False,
        blank=False,
        default=0
    )

    score_yellow = models.DecimalField(
        help_text=_('The score of user with latest "We need food or supplies" status in this grid'),
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )

    count_yellow = models.SmallIntegerField(
        help_text=_('The number of user with latest "We need food or supplies" status'),
        null=False,
        blank=False,
        default=0
    )

    score_red = models.DecimalField(
        help_text=_('The score of user with latest "We need medical help" status in this grid'),
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )

    count_red = models.SmallIntegerField(
        help_text=_('The number of user with latest "We need medical help" status in this grid'),
        null=False,
        blank=False,
        default=0
    )

    population = models.IntegerField(
        help_text=_('Number of people in this grid'),
        null=False,
        blank=False,
        default=300
    )

    total_score = models.DecimalField(
        help_text=_('Total score of this grid'),
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.id, self.geometry, self.population, self.total_score)

    def set_color_score(self, color="green"):
        score = color_score_km_grid(self.count_green, self.population, color)
        setattr(self, f'score_{color}', score)
        self.save()

    def set_total_core(self):
        total_score = status_score_km_grid(
            self.count_green,
            self.count_yellow,
            self.count_red,
            self.population,
        )

        self.total_score = total_score
        self.save()

    class Meta:
        # Set managed to False because this model will access existing Materialized Views
        managed = False
        ordering = ('-id',)
