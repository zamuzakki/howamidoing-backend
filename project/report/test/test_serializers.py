from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from nose.tools import eq_, ok_
from .factories import StatusFactory
from ..serializers import StatusSerializer


class TestStatusSerializer(TestCase):

    def setUp(self):
        self.user_data = model_to_dict(StatusFactory.build())

    def test_serializer_with_empty_data(self):
        serializer = StatusSerializer(data={})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = StatusSerializer(data=self.user_data)
        ok_(serializer.is_valid())