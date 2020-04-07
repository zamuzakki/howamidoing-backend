from django.urls import reverse
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status as http_status
from faker import Faker
import factory
from ..models import Status
from .factories import StatusFactory
from project.users.test.factories import UserFactory
import sys

fake = Faker()


class TestStatusListTestCase(APITestCase):
    """
    Tests /statuss list operations.
    """

    def setUp(self):
        self.url = reverse('status-list')
        self.user = UserFactory()
        self.status_data = factory.build(dict, FACTORY_CLASS=StatusFactory)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

    def test_post_request_with_no_field_no_data_fails(self):
        response = self.client.post(self.url, {})
        eq_(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_field_no_data_fails(self):
        response = self.client.post(self.url, {"name":"","description":""})
        eq_(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.status_data)
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        status = Status.objects.get(pk=response.data.get('id'))
        eq_(status.name, self.status_data.get('name'))
        eq_(status.description, self.status_data.get('description'))


class TestStatusDetailTestCase(APITestCase):
    """
    Tests /status detail operations.
    """

    def setUp(self):
        self.status = StatusFactory()
        self.user = UserFactory()
        self.url = reverse('status-detail', kwargs={'pk': self.status.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

    def test_get_request_returns_a_given_status(self):
        response = self.client.get(self.url)
        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_put_request_updates_a_status(self):
        new_name = fake.name()
        payload = {'name': new_name}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, http_status.HTTP_200_OK)

        status = Status.objects.get(pk=self.status.id)
        eq_(status.name, new_name)
