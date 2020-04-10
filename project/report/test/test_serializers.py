from django.test import TestCase
from django.forms.models import model_to_dict
from nose.tools import eq_, ok_
from .factories import StatusFactory, ReportFactory
from ..serializers import StatusSerializer, ReportSerializer


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

    def test_serializer_with_empty_data(self):
        serializer = ReportSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        pass
