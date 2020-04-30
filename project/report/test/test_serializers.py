from django.test import TestCase
from django.forms.models import model_to_dict
from nose.tools import eq_, ok_
from .factories import StatusFactory, ReportFactory
from ..serializers import StatusSerializer, ReportSerializer, \
    ReportCreateUpdateSerializer, KmGridSerializer


class TestStatusSerializer(TestCase):

    def setUp(self):
        self.status_data = model_to_dict(StatusFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = StatusSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = StatusSerializer(data=self.status_data)
        ok_(serializer.is_valid(), True)

class TestReportSerializer(TestCase):

    def setUp(self):
        self.report_data = ReportFactory()

        self.location = self.report_data.location
        self.report_data_json = {
            "location": {
                "type": "Point",
                "coordinates": [
                    self.location.x,
                    self.location.y
                ]
            },
            "status": self.report_data.status.id,
            "user": self.report_data.user.id,
        }

    def test_serializer_with_empty_data(self):
        serializer = ReportSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_create_update_serializer_with_empty_data(self):
        serializer = ReportCreateUpdateSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_create_update_serializer_with_valid_data(self):
        serializer = ReportCreateUpdateSerializer(data=self.report_data_json)
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
            "population": 0
        }

    def test_serializer_with_empty_data(self):
        serializer = KmGridSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = KmGridSerializer(data=self.data)
        eq_(serializer.is_valid(), True)
