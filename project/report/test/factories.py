from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos import fromstr
from faker.providers import BaseProvider
import factory
import factory.fuzzy
import json
from django.conf import settings
from django.utils.timezone import now

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.User'
        django_get_or_create = ('id',)

    id = factory.Faker('uuid4')


class StatusFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'report.Status'
        django_get_or_create = ('name', 'description',)

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f'Status {n}')
    description = factory.Sequence(lambda n: f'Description {n}')


def get_grid_from_file(index=0):
    with open(settings.BASE_DIR + '/../example/grid.geojson', 'r') as f:
        content = f.read()
        data = json.loads(content)['features']
        return fromstr(json.dumps(data[index]['geometry']))


class KmGridFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'report.KmGrid'
        django_get_or_create = ('geometry',)

    id = factory.Sequence(lambda n: n)
    geometry = factory.Sequence(get_grid_from_file)
    population = factory.Sequence(lambda n: n+1)


class DjangoGeoPointProvider(BaseProvider):
    def geo_point(self, **kwargs):
        kwargs.pop('coords_only', None)
        faker = factory.Faker('local_latlng', coords_only=True, **kwargs)
        coords = faker.generate()
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


class ReportFactory(factory.django.DjangoModelFactory):

    id = factory.Sequence(lambda n: n)
    grid = factory.SubFactory(KmGridFactory)
    status = factory.SubFactory(StatusFactory)
    timestamp = factory.LazyFunction(now)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'report.Report'
        django_get_or_create = ('grid', 'status', 'timestamp', 'user')
