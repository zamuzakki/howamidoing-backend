from django.urls import reverse
from django.core.paginator import Paginator
from nose.tools import eq_
from rest_framework.test import APITestCase
from rest_framework import status as http_status
from faker import Faker
from project.report.models.user import User
from project.report.test.factories import UserFactory
from project.users.test.factories import UserAdminFactory

import factory


fake = Faker()

class TestUserBaseClass(APITestCase):
    """
    Base Class for User test case.
    """

    def setUpTestData(cls):
        """
        Set base data for all test case
        """
        cls.user_admin = UserAdminFactory()
        cls.user = factory.build(dict, FACTORY_CLASS=UserFactory)

    def set_user_admin_credential(self):
        """
        Set admin user credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_admin.auth_token}')


class TestUserListTestCase(TestUserBaseClass):
    """
    Tests /user list operations.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Before TestCase is run, set some data.
        """
        return super().setUpTestData(cls)

    def setUp(self):
        """
        Set data for this test case.
        """
        self.url = reverse('user-list')

    def test_create_user_succeeds(self):
        """
        Create anonymous user
        """
        response = self.client.post(self.url)
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        user = User.objects.first()
        eq_(response.data.get('id'), str(user.id))

    def test_list_user_failed_as_anonymous_user(self):
        """
        List User as anonymous user.
        Response status-code should be 403 Forbidden and the length
        should be the same between reponse and queryset.
        """
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_list_user_succeeds_as_admin_user(self):
        """
        List User as admin user.
        Response status-code should be 200 OK and the length should be the same between reponse and queryset.
        """
        self.set_user_admin_credential()
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_200_OK)

        user_qs = User.objects.all()
        user_qs_page_1 = Paginator(user_qs, 1)
        eq_(response.data.get('count'), user_qs_page_1.count)
