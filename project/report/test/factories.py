import factory


class StatusFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'report.Status'
        django_get_or_create = ('name', 'description',)

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: f'Status {n}')
    description = factory.Sequence(lambda n: f'Description {n}')