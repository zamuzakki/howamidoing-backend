from django.urls import reverse
from django.contrib.auth.hashers import check_password
from nose.tools import ok_, eq_
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
import factory
from ..models import User
from .factories import UserFactory, UserAdminFactory

fake = Faker()


class TestUserListTestCase(APITestCase):
    """
    Tests /users list operations.
    """

    def setUp(self):
        self.url = reverse('user-list')
        self.status_data = factory.build(dict, FACTORY_CLASS=UserFactory)

    def test_create_user_with_no_data_fails(self):
        """
        Create new User without data.
        Response should be 400 Bad Request.
        """
        response = self.client.post(self.url, {})
        eq_(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_with_valid_data_succeeds(self):
        """
        Create new User with valid data.
        Response should be 201 Created.
        """
        response = self.client.post(self.url, self.status_data)
        eq_(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=response.data.get('id'))
        eq_(user.username, self.status_data.get('username'))
        ok_(check_password(self.status_data.get('password'), user.password))


class TestUserDetailTestCase(APITestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.user_admin = UserAdminFactory()

    def test_retrieve_user(self):
        """
        Retrieve User with valid data.
        Response should be 200 OK.
        """
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        response = self.client.get(self.url)
        eq_(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """
        Update User with valid data.
        Response should be 200 OK and User first_name should be updated.
        """
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        new_first_name = fake.first_name()
        payload = {'first_name': new_first_name}
        response = self.client.put(self.url, payload)
        eq_(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.id)
        eq_(user.first_name, new_first_name)
