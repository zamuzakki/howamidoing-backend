from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.gis.db.models.functions import Centroid
from ..models.km_grid import KmGrid
from nose.tools import eq_, ok_
from .factories import StatusFactory, ReportFactory, UserFactory
from ..serializers import StatusSerializer, ReportSerializer, \
    ReportCreateSerializer, KmGridSerializer, KmGridScoreSerializer, UserSerializer

class TestUserSerializer(TestCase):
    def setUp(self):
        self.user_data = model_to_dict(UserFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = UserSerializer(data={})
        eq_(serializer.is_valid(), True)

class TestStatusSerializer(TestCase):

    def setUp(self):
        self.status_data = model_to_dict(StatusFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = StatusSerializer(data={"name": "", "description": ""})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = StatusSerializer(data=self.status_data)
        ok_(serializer.is_valid(), True)

class TestReportSerializer(TestCase):

    def setUp(self):
        self.report_data = ReportFactory()

        self.geometry = self.report_data.grid.geometry
        self.centroid = KmGrid.objects.annotate(centroid=Centroid('geometry'))[0].centroid

        self.report_data_json = {
            "grid": self.report_data.grid.id,
            "status": self.report_data.status.id,
            "user": self.report_data.user.id,
        }

        self.report_create_data_json = {
            "location": {
                "type": "Point",
                "coordinates": [
                    self.centroid.x,
                    self.centroid.y
                ]
            },
            "status": self.report_data.status.id,
            "user": self.report_data.user.id,
        }

    def test_serializer_with_empty_data(self):
        serializer = ReportSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_data(self):
        serializer = ReportSerializer(data=self.report_data_json)
        eq_(serializer.is_valid(), True)

    def test_create_serializer_with_empty_data(self):
        serializer = ReportCreateSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_create_serializer_with_data(self):
        serializer = ReportCreateSerializer(data=self.report_create_data_json)
        eq_(serializer.is_valid(), True)


class TestKmGridSerializer(TestCase):

    def setUp(self):
        self.data = {
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [18.40417142576775, -33.922105319969859],
                        [18.413154578608943, -33.922105319969859],
                        [18.413154578608943, -33.929559187481644],
                        [18.40417142576775, -33.929559187481644],
                        [18.40417142576775, -33.922105319969859]
                    ]
                ]
            },
            "population": 1
        }

    def test_serializer_with_valid_data(self):
        serializer = KmGridSerializer(data=self.data)
        eq_(serializer.is_valid(), True)


class TestKmGridScoreSerializer(TestCase):

    def setUp(self):
        self.data = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            18.40417142576775,
                            -33.92210531996986
                        ],
                        [
                            18.413154578608943,
                            -33.92210531996986
                        ],
                        [
                            18.413154578608943,
                            -33.929559187481644
                        ],
                        [
                            18.40417142576775,
                            -33.929559187481644
                        ],
                        [
                            18.40417142576775,
                            -33.92210531996986
                        ]
                    ]
                ]
            },
            "properties": {
                "total_score": "0.00"
            }
        }

    def test_serializer_with_valid_data(self):
        serializer = KmGridScoreSerializer(data=self.data)
        eq_(serializer.is_valid(), True)
