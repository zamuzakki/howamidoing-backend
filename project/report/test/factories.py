from django.contrib.gis.geos.point import Point
from faker.providers import BaseProvider
from project.users.test.factories import UserFactory
import factory
from django.utils.timezone import now

class StatusFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'report.Status'
        django_get_or_create = ('name', 'description',)

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f'Status {n}')
    description = factory.Sequence(lambda n: f'Description {n}')


class DjangoGeoPointProvider(BaseProvider):

    def geo_point(self, **kwargs):
        kwargs.pop('coords_only', None)
        faker = factory.Faker('local_latlng', coords_only=True, **kwargs)
        coords = faker.generate()
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)


class ReportFactory(factory.django.DjangoModelFactory):
    factory.Faker.add_provider(DjangoGeoPointProvider)

    class Meta:
        model = 'report.Report'
        django_get_or_create = ('location', 'status', 'timestamp', 'user')

    id = factory.Sequence(lambda n: n)
    location = factory.Faker('geo_point')
    status = factory.SubFactory(StatusFactory)
    timestamp = factory.LazyFunction(now)
    user = factory.SubFactory(UserFactory)
