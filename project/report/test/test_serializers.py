from nose.tools import eq_, ok_

from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.gis.db.models.functions import Centroid
from project.report.models.km_grid import KmGrid
from project.report.test.factories import StatusFactory, ReportFactory, UserFactory
from project.report.serializers import StatusSerializer, ReportSerializer, \
    ReportCreateSerializer, UserSerializer

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
