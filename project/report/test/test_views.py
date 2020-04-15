from django.urls import reverse
from django.core.paginator import Paginator
from nose.tools import eq_, assert_not_equal
from rest_framework.test import APITestCase
from rest_framework import status as http_status
from faker import Faker
import factory
from ..models import Status
from .factories import StatusFactory, ReportFactory
from project.users.test.factories import UserFactory, UserAdminFactory

fake = Faker()

class TestStatusBaseClass(APITestCase):
    """
    Base Class for Status test case.
    """

    def setUpTestData(cls):
        """
        Set base data for all test case
        """
        cls.user = UserFactory()
        cls.user_admin = UserAdminFactory()
        cls.status_data = factory.build(dict, FACTORY_CLASS=StatusFactory)
        cls.status = StatusFactory()

    def set_user_regular_credential(self):
        """
        Set regular user credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

    def set_user_admin_credential(self):
        """
        Set admin user credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_admin.auth_token}')


class TestStatusListTestCase(TestStatusBaseClass):
    """
    Tests /status list operations.
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
        self.url = reverse('status-list')

    def post_request_with_data(self, data):
        """
        Send POST request with data to defined URL.
        """
        response = self.client.post(self.url, data)
        return response

    def test_create_status_with_empty_data_fails_as_admin_user(self):
        """
        Create new Status using post request with empty data as admin user.
        Response status-code should be 400 Bad Request.
        """
        self.set_user_admin_credential()
        response = self.post_request_with_data({})
        eq_(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_create_status_with_empty_data_fails_as_non_admin_user(self):
        """
        Create new Status using post request with empty data as regular user.
        Response status-code should be 400 Bad Request.
        """
        self.set_user_regular_credential()
        response = self.post_request_with_data({})
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_create_status_with_valid_data_succeeds_as_admin_user(self):
        """
        Create new Status using post request with valid data as admin user.
        Response status-code should be 201 Created,
        """
        self.set_user_admin_credential()
        response = self.post_request_with_data(self.status_data)
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        status = Status.objects.get(pk=response.data.get('id'))
        eq_(status.name, self.status_data.get('name'))
        eq_(status.description, self.status_data.get('description'))

    def test_create_status_with_valid_data_fails_as_non_admin_user(self):
        """
        Create new Status using post request with valid data as regular user.
        Response status-code should be 403 Forbidden.
        """
        self.set_user_regular_credential()
        response = self.post_request_with_data(self.status_data)
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_list_status_succeeds_as_regular_user(self):
        """
        List Status as regular user.
        Response status-code should be 200 OK and the length should be the same between reponse and queryset.
        """
        self.set_user_regular_credential()
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_200_OK)

        status_qs = Status.objects.all()
        status_qs_page_1 = Paginator(status_qs, 1)
        eq_(response.data.get('count'), status_qs_page_1.count)


class TestStatusDetailTestCase(TestStatusBaseClass):
    """
    Tests /status detail operations.
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
        self.url = reverse('status-detail', kwargs={'pk': self.status.pk})

    def put_request_valid_data(self):
        """
        Send PUT request with data to defined URL.
        :returns (response data, new_name for the status)
        """
        new_name = fake.name()
        payload = {'name': new_name}
        response = self.client.put(self.url, payload)
        return (response, new_name)

    def delete_request_valid_data(self, data):
        """
        Send DELETE request with data to defined URL.
        :return response data
        """
        response = self.client.delete(self.url, data)
        return response

    def test_retrieve_status_as_admin_user(self):
        """
        Retrieve Status details as admin user.
        Response status-code should be 200 OK.
        """
        self.set_user_regular_credential()
        response = self.client.get(self.url)
        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_update_a_status_succeeds_as_admin_user(self):
        """
        Update Status details as admin user.
        Response status-code should be 200 OK and Status name should be updated.
        """
        self.set_user_admin_credential()
        response, new_name = self.put_request_valid_data()
        eq_(response.status_code, http_status.HTTP_200_OK)

        status = Status.objects.get(pk=self.status.id)
        eq_(status.name, new_name)

    def test_update_a_status_fails_as_regular_user(self):
        """
        Update Status details as regular user.
        Response status-code should be 403 Forbidden and Status name should not be updated
        """
        self.set_user_regular_credential()
        response, new_name = self.put_request_valid_data()
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

        status = Status.objects.get(pk=self.status.id)
        assert_not_equal(status.name, new_name)

    def test_delete_a_status_succeeds_as_admin_user(self):
        """
        Delete Status as admin user.
        Response status-code should be 204 No Content and Status be deleted.
        """
        self.set_user_admin_credential()

        response = self.delete_request_valid_data(data={'id': self.status.id})
        eq_(response.status_code, http_status.HTTP_204_NO_CONTENT)

        status = Status.objects.filter(id=self.status.id)
        eq_(status.count(), 0)

    def test_delete_a_status_fails_as_regular_user(self):
        """
        Delete Status details as regular user.
        Response status-code should be 403 Forbidden and Status should not be deleted
        """
        self.set_user_regular_credential()
        response = self.delete_request_valid_data(data={'id': self.status.id})
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

        status = Status.objects.filter(pk=self.status.id)
        eq_(status.count(), 1)


class TestReportBaseClass(APITestCase):
    """
    Base Class for Report test case.
    """

    def setUpTestData(cls):
        """
        Set base data for all test case
        """
        cls.status_1 = StatusFactory()
        cls.status_2 = StatusFactory()

        cls.user_1 = UserFactory()
        cls.user_2 = UserFactory()

        cls.report_1_data_dict = factory.build(dict, FACTORY_CLASS=ReportFactory)
        cls.report_2_data_dict = factory.build(dict, FACTORY_CLASS=ReportFactory)

        cls.report_1_data_for_create_update = {
            "status": cls.report_1_data_dict.get('status').id,
            "user": cls.report_1_data_dict.get('user').id,
            "location": {
                "type": "Point",
                "coordinates": [
                    cls.report_1_data_dict.get('location').x,
                    cls.report_1_data_dict.get('location').y,
                ]
            }
        }

        cls.report_1 = ReportFactory()
        cls.report_2 = ReportFactory()

    def set_user_1_credential(self):
        """
        Set user_1 credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')

    def set_user_2_credential(self):
        """
        Set user_2 credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')


class TestReportListTestCase(TestReportBaseClass):
    """
    Tests /report list operations.
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
        self.url = reverse('report-list')

    def post_request_with_data(self, data):
        """
        Send POST request with data to defined URL.
        """
        response = self.client.post(self.url, data, format='json')
        return response

    def test_create_report_with_empty_data_succeeds_as_user(self):
        """
        Create new Report using post request with empty data as user.
        Response status-code should be 400 Bad Request.
        """
        pass

    def test_create_report_with_valid_data_succeeds_as_user(self):
        """
        Create new Report using post request with valid data as user.
        Response status-code should be 201 Created the length should be the same between reponse and queryset.
        """
        pass
