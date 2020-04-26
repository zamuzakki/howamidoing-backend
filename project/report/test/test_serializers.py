from django.test import TestCase
from django.forms.models import model_to_dict
from nose.tools import eq_, ok_
from .factories import StatusFactory, ReportFactory
from ..serializers import StatusSerializer, ReportSerializer
import json


class TestStatusSerializer(TestCase):

    def setUp(self):
        self.status_data = model_to_dict(StatusFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = StatusSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = StatusSerializer(data=self.status_data)
        ok_(serializer.is_valid())

class TestReportSerializer(TestCase):

    def setUp(self):
        self.report_data = model_to_dict(ReportFactory.build())
        self.location = self.report_data['location']
        self.report_data_json = json.dumps({
            "location": {
                "type": "Point",
                "coordinates": [
                    self.location.x,
                    self.location.y
                ]
            },
            "status": self.report_data['status'],
            "user": self.report_data['user'],
        })

    def test_serializer_with_empty_data(self):
        serializer = ReportSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        pass
