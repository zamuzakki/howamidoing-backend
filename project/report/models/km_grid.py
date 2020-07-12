from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db import models as gis
from django.db import models
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger(__name__)

class KmGridQuerySet(models.QuerySet):
    """Custom version manager for Grid."""

    def geometry_contains(self, geojson_geometry_string):
        print(geojson_geometry_string)
        geometry = GEOSGeometry(
            "POINT({} {})".format(
                geojson_geometry_string['coordinates'][0],
                geojson_geometry_string['coordinates'][1]
            ),
            srid=3857
        )
        print(geometry)
        return self.filter(
            geometry__contains=geometry
        )

    def geometry_equals(self, geojson_geometry_string):
        geometry = GEOSGeometry(geojson_geometry_string, srid=3857)
        return self.filter(
            geometry__equals=geometry
        )


class KmGrid(models.Model):
    """
    Model representing grid and its population number.
    Data will be generated using Positgis and Worldpop.
    """
    geometry = gis.PolygonField(
        help_text=_('Geometry of this grid'),
        null=True,
        blank=True,
        default=None,
        srid=3857
    )

    population = models.IntegerField(
        help_text=_('Number of people in this grid'),
        null=False,
        blank=False,
        default=300
    )

    objects = KmGridQuerySet().as_manager()

    def __str__(self):
        return '{} | {} | {}'.format(self.id, self.geometry, self.population)

    class Meta:
        managed = True
        ordering = ('-id',)
