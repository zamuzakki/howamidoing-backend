from django.contrib.gis.geos import fromstr
from django.contrib.gis.db import models as gis
from django.utils.translation import ugettext_lazy as _
from project.report.utils.scoring_grid import color_score_km_grid, status_score_km_grid
from django.core.exceptions import FieldError
from django.contrib.gis.db import models
from rest_framework.serializers import ValidationError
from rest_framework_mvt.managers import MVTManager

import logging

logger = logging.getLogger(__name__)


class KmGridScoreQuerySet(models.QuerySet):
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


class KmGridScoreManager(models.Manager):
    """Custom version manager for Grid Score."""

    def get_queryset(self):
        return KmGridScoreQuerySet(self.model, using=self._db)

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


class KmGridScoreMVTManager(MVTManager):

    def intersect(self, bbox="", limit=-1, offset=0, filters={}):
        """
        Args:
            bbox (str): A string representing a bounding box, e.g., '-90,29,-89,35'.
            limit (int): Number of entries to include in the result.  The default
                         is -1 (includes all results).
            offset (int): Index to start collecting entries from.  Index size is the limit
                          size.  The default is 0.
            filters (dict): The keys represent column names and the values represent column
                            values to filter on.
        Returns:
            bytes:
            Bytes representing a Google Protobuf encoded Mapbox Vector Tile.  The
            vector tile will store each applicable row from the database as a
            feature.  Applicable rows fall within the passed in bbox.

        Raises:
            ValidationError: If filters include keys or values not accepted by
                             the manager's model.

        Note:
            The sql execution follows the guidelines from Django below.  As suggested, the executed
            query string does NOT contain quoted parameters.

            https://docs.djangoproject.com/en/2.2/topics/db/sql/#performing-raw-queries
        """
        limit = "ALL" if limit == -1 else limit
        query, parameters = self._build_query(filters=filters)
        with self._get_connection().cursor() as cursor:
            cursor.execute(query, [str(bbox), str(bbox)] + parameters + [limit, offset])
            mvt = cursor.fetchall()[-1][-1]  # should always return one tile on success
        return mvt

    def _create_select_statement(self):
        """
        Create a SELECT statement that only includes columns defined on the
        model.  Each column must be named in the SELECT statement to specify
        only the required columns.  Including the geom column raises an error
        in the PostGIS ST_AsMVT function.

        Returns:
            str:
            A string representing a parameterized SQL query SELECT statement.
        """

        # Use this if we want to show all columns
        # columns = self._get_non_geom_columns()
        columns = ['id', 'population', 'total_report', 'total_score']
        sql, _ = self.only(*columns).query.sql_with_params()
        select_sql = sql.split("FROM")[0].lstrip("SELECT ").strip() + ","
        return select_sql

    def _build_query(self, filters={}):
        """
        Args:
            filters (dict): keys represent column names and values represent column
                            values to filter on.
        Returns:
            tuple:
            A tuple of length two.  The first element is a string representing a
            parameterized SQL query.  The second element is a list of parameters
            used as inputs to the query's WHERE clause.
        """
        table = self.model._meta.db_table.replace('"', "")
        select_statement = self._create_select_statement()
        (
            parameterized_where_clause,
            where_clause_parameters,
        ) = self._create_where_clause_with_params(table, filters)
        query = f"""
        SELECT NULL AS id, ST_AsMVT(q, 'default', 4096, 'mvt_geom')
            FROM (SELECT {select_statement}
                ST_AsMVTGeom({table}.{self.geo_col},
                ST_GeomFromText(%s), 4096, 0, false) AS mvt_geom
            FROM {table}
            WHERE {parameterized_where_clause}
            LIMIT %s
            OFFSET %s) AS q;
        """
        return (query.strip(), where_clause_parameters)

    def _create_where_clause_with_params(self, table, filters):
        """
        Args:
            table (str): A string representing the name of the table to query on.
            filters (dict): keys represent column names and values represent column
                            values to filter on.
        Returns:
            tuple:
            A tuple of length two.  The first element is a string representing a
            parameterized SQL query WHERE clause.  The second element is a list
            of parameters used as inputs to the WHERE clause.
        """
        try:
            sql, params = self.filter(**filters).query.sql_with_params()
        except FieldError as error:
            raise ValidationError(str(error))
        extra_wheres = " AND " + sql.split("WHERE")[1].strip() if params else ""
        where_clause = (
            f"ST_Intersects({table}.{self.geo_col}, "
            f"ST_GeomFromText(%s)){extra_wheres}"
        )
        return where_clause, list(params)


class KmGridScore(models.Model):
    """
    Model for user status summary per grid
    """
    geometry = gis.PolygonField(
        help_text=_('Geometry of this Grid'),
        null=True,
        blank=True,
        default=None,
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

    objects = KmGridScoreManager()
    vector_tiles = KmGridScoreMVTManager(geo_col='geometry')

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
