from django.contrib.gis.geos import fromstr
from django.contrib.gis.db import models as gis
from django.db import models
from django.utils.translation import ugettext_lazy as _
from ..utils.scoring_grid import color_score_km_grid, status_score_km_grid
from rest_framework_mvt.managers import MVTManager

import logging

logger = logging.getLogger(__name__)

class KmGridScoreQuerySet(models.QuerySet):
    """Custom version manager for Grid."""

    def geometry_contains(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=4326)
        return self.filter(
            geometry__contains=geometry
        )

    def geometry_equals(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=4326)
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


class KmGridScoreManager(models.Manager):
    """Custom version manager for Grid Score."""

    def get_queryset(self):
        return KmGridScoreQuerySet(self.model, using=self._db)

    def geometry_contains(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=4326)
        return self.get_queryset().filter(
            geometry__contains=geometry
        )

    def geometry_equals(self, geojson_geometry_string):
        geometry = fromstr(geojson_geometry_string, srid=4326)
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

    objects = KmGridScoreManager()
    vector_tiles = MVTManager(geo_col='geometry')

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
        # Set managed to False because this model will access existing Materialized Views
        managed = True
        ordering = ('-id',)
