from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos import Polygon
from faker.providers import BaseProvider
from ..utils.scoring_grid import color_score_km_grid, status_score_km_grid
import factory
import factory.fuzzy
import random
import json
from django.conf import settings
from django.utils.timezone import now

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.User'
        django_get_or_create = ('id',)

    id = factory.Faker('uuid4')


STATUS_NAME = ['All Well Here', 'Need Food or Supplies', 'Need Medical Help']
class StatusFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'report.Status'
        django_get_or_create = ('name', 'description',)

    id = factory.Sequence(lambda n: n)
    name = factory.fuzzy.FuzzyChoice(STATUS_NAME)
    description = factory.Sequence(lambda n: f'Description {n}')


def get_grid_from_file(index=0):
    with open(settings.BASE_DIR + '/../example/grid.geojson', 'r') as f:
        content = f.read()
        data = json.loads(content)['features']
        grid = data[index]['geometry']
        geom = Polygon((
            (grid['coordinates'][0][0][0], grid['coordinates'][0][0][1]),
            (grid['coordinates'][0][1][0], grid['coordinates'][0][1][1]),
            (grid['coordinates'][0][2][0], grid['coordinates'][0][2][1]),
            (grid['coordinates'][0][3][0], grid['coordinates'][0][3][1]),
            (grid['coordinates'][0][4][0], grid['coordinates'][0][4][1]),
        ), srid=3857)
        return geom


class KmGridFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.KmGrid'
        django_get_or_create = ('geometry',)

    id = factory.Sequence(lambda n: n)
    geometry = factory.Sequence(get_grid_from_file)
    population = factory.Sequence(lambda n: n+1)


class KmGridScoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.KmGridScore'
        django_get_or_create = ('geometry',)

    id = factory.Sequence(lambda n: n)
    geometry = factory.Sequence(get_grid_from_file)
    population = factory.LazyAttribute(lambda o: random.randrange(1, 100))
    count_green = factory.LazyAttribute(lambda o: random.randrange(1, o.population))
    score_green = factory.LazyAttribute(lambda o: color_score_km_grid(o.count_green, o.population, 'green'))
    count_yellow = factory.LazyAttribute(lambda o: random.randrange(1, o.population))
    score_yellow = factory.LazyAttribute(
        lambda o: color_score_km_grid(o.count_yellow, o.population, 'yellow')
    )
    count_red = factory.LazyAttribute(lambda o: random.randrange(1, o.population))
    score_red = factory.LazyAttribute(lambda o: color_score_km_grid(o.count_red, o.population, 'red'))
    total_report = factory.LazyAttribute(lambda o: o.count_green + o.count_yellow + o.count_red)
    total_score = factory.LazyAttribute(lambda o: status_score_km_grid(
        o.count_green,
        o.count_yellow,
        o.count_red,
        o.population
    ))


class DjangoGeoPointProvider(BaseProvider):
    def geo_point(self, **kwargs):
        kwargs.pop('coords_only', None)
        faker = factory.Faker('local_latlng', coords_only=True, **kwargs)
        coords = faker.generate()
        return Point(x=float(coords[1]), y=float(coords[0]), srid=3857)


class ReportFactory(factory.django.DjangoModelFactory):

    id = factory.Sequence(lambda n: n)
    grid = factory.SubFactory(KmGridFactory)
    status = factory.SubFactory(StatusFactory)
    timestamp = factory.LazyFunction(now)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'report.Report'
        django_get_or_create = ('grid', 'status', 'timestamp', 'user')
