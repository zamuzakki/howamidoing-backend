from django.contrib.gis.geos import fromstr
from django.contrib.gis.db import models as gis
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..utils.scoring_grid import color_score_km_grid, status_score_km_grid

import logging

logger = logging.getLogger(__name__)


class ReportPointScoreQuerySet(models.QuerySet):
    """Custom version manager for Grid."""

    def geometry_contains(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=3857)
        return self.filter(
            geometry__contains=geometry
        )

    def geometry_equals(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=3857)
        return self.filter(
            geometry__equals=geometry
        )

    def green_grid(self):
        return self.filter(total_score=0)

    def yellow_grid(self):
        return self.filter(total_score=1)

    def red_grid(self):
        return self.filter(total_score=2)

    def grid_with_report(self):
        return self.filter(total_report__gt=0)


class ReportPointScoreManager(models.Manager):
    """Custom version manager for Grid Score."""

    def get_queryset(self):
        return ReportPointScoreQuerySet(self.model, using=self._db)

    def geometry_contains(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=3857)
        return self.get_queryset().filter(
            geometry__contains=geometry
        )

    def geometry_equals(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=3857)
        return self.get_queryset().filter(
            geometry__equals=geometry
        )

    def green_grid(self):
        return self.get_queryset().filter(total_score=0)

    def yellow_grid(self):
        return self.get_queryset().filter(total_score=1)

    def red_grid(self):
        return self.get_queryset().filter(total_score=2)

    def grid_with_report(self):
        return self.get_queryset().filter(total_report__gt=0)


class ReportPointScore(models.Model):
    """
    Summary of use's report scoring in certain area.
    """
    location = gis.PointField(
        help_text=_('Centroid of the area where calculation takes place'),
        srid=3857
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

    total_report = models.SmallIntegerField(
        help_text=_('The number of all report in the grid'),
        null=False,
        blank=False,
        default=0
    )

    total_score = models.DecimalField(
        help_text=_('Total score of this grid'),
        max_digits=7,
        decimal_places=2,
        null=False,
        blank=False,
        default=0
    )

    objects = ReportPointScoreManager()

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.id, self.geometry, self.population, self.total_score)

    def set_color_score(self, color="green"):
        score = color_score_km_grid(getattr(self, f'count_{color}'), self.population, color)
        setattr(self, f'score_{color}', score)
        self.save()

    def set_color_score_by_status(self, status):
        if "well" in status.name:
            self.set_color_score('green')
        elif "supplies" in status.name:
            self.set_color_score('yellow')
        elif "medical" in status.name:
            self.set_color_score('red')

    def set_color_count_by_status(self, status, operation='add'):

        if "well" in status.name:
            if operation == 'add':
                self.count_green += 1
            if operation == 'sub':
                self.count_green -= 1
        elif "supplies" in status.name:
            if operation == 'add':
                self.count_yellow += 1
            if operation == 'sub':
                self.count_yellow -= 1
        elif "medical" in status.name:
            if operation == 'add':
                self.count_red += 1
            if operation == 'sub':
                self.count_red -= 1
        self.save()

    def set_total_score(self):
        total_score = status_score_km_grid(
            self.count_green,
            self.count_yellow,
            self.count_red,
            self.population,
        )

        self.total_score = total_score
        self.save()

    class Meta:
        managed = True
        ordering = ('-id',)
