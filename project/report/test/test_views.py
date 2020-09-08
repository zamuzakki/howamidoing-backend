from django.urls import reverse
from django.contrib.gis.db.models.functions import Centroid
from django.core.paginator import Paginator
from nose.tools import eq_
from rest_framework.test import APITestCase
from rest_framework import status as http_status
from faker import Faker
from project.report.models.status import Status
from project.report.models.user import User
from project.report.models.report import Report
from project.report.models.km_grid import KmGrid
from project.report.test.factories import StatusFactory, ReportFactory, UserFactory, KmGridFactory
from project.users.test.factories import UserAdminFactory

import factory


fake = Faker()

class TestStatusBaseClass(APITestCase):
    """
    Base Class for Status test case.
    """

    def setUpTestData(cls):
        """
        Set base data for all test case
        """
        cls.user_admin = UserAdminFactory()
        cls.status_data = factory.build(dict, FACTORY_CLASS=StatusFactory)
        cls.status = StatusFactory()

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

    def test_list_status_succeeds_as_regular_user(self):
        """
        List Status as regular user.
        Response status-code should be 200 OK and the length should be the same between response and queryset.
        """
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_200_OK)

        status_qs = Status.objects.all()
        status_qs_page_1 = Paginator(status_qs, 1)
        eq_(response.data.get('count'), status_qs_page_1.count)

    def test_list_status_succeeds_as_admin_user(self):
        """
        List Status as admin user.
        Response status-code should be 200 OK and the length should be the same between reponse and queryset.
        """
        self.set_user_admin_credential()
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

    def test_retrieve_status_as_admin_user(self):
        """
        Retrieve Status details as admin user.
        Response status-code should be 200 OK.
        """
        self.set_user_admin_credential()
        response = self.client.get(self.url)
        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_retrieve_status_as_regular_user(self):
        """
        Retrieve Status details as regular user.
        Response status-code should be 200 OK.
        """
        response = self.client.get(self.url)
        eq_(response.status_code, http_status.HTTP_200_OK)


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


class TestReportBaseClass(APITestCase):
    """
    Base Class for Report test case.
    """

    def setUpTestData(cls):
        """
        Set base data for all test case
        """
        cls.user_1 = UserFactory()
        cls.user_admin = UserAdminFactory()

        cls.status_1 = StatusFactory()
        cls.status_2 = StatusFactory()

        cls.grid_1 = KmGridFactory()
        cls.centroid_1 = KmGrid.objects.filter(id=cls.grid_1.id).\
            annotate(centroid=Centroid('geometry'))[0].centroid
        cls.report_1_json = {
            "location": {
                "type": "Point",
                "coordinates": [
                    cls.centroid_1.x,
                    cls.centroid_1.y
                ]
            },
            "status": cls.status_1.id,
            "user": cls.user_1.id,
        }

        cls.grid_2 = KmGridFactory()
        cls.centroid_2 = KmGrid.objects.filter(id=cls.grid_2.id).\
            annotate(centroid=Centroid('geometry'))[0].centroid
        cls.report_2_json = {
            "location": {
                "type": "Point",
                "coordinates": [
                    cls.centroid_2.x,
                    cls.centroid_2.y
                ]
            },
            "status": cls.status_2.id,
            "user": cls.user_1.id,
        }

        cls.report_3 = ReportFactory()

    def set_user_admin_credential(self):
        """
        Set admin user credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_admin.auth_token}')


class TestReportListTestCase(TestReportBaseClass):
    """
    Tests /report list operations.
    """

    data = dict()

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

    def test_create_report_with_empty_data_fails_as_regular_user_1(self):
        """
        Create new Report using post request with empty data as regular user.
        Response status-code should be 500 Internal Server Error.
        """
        response = self.post_request_with_data({})
        eq_(response.status_code, http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_create_self_report_with_valid_data_succeeds_as_regular_user(self):
        """
        Create new Report using post request with valid data as regular user.
        Then, we create another report for the user. It should mark the first report as non current.
        Response status-code should be 201 Created and the attributes should match.
        """
        response = self.post_request_with_data(self.report_1_json)
        report_1 = response.data
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        report = Report.objects.get(pk=response.data['id'])
        eq_(report.user.id, response.data['user'])
        eq_(report.status.id, response.data['status'])
        eq_(response.data['current'], True)
        eq_(report.current, True)

        # Create new report fot the user
        self.post_request_with_data(self.report_2_json)

        # Previous report `current` field must be False
        report_1 = Report.objects.get(id=report_1['id'])
        eq_(report_1.current, False)

    def test_list_report_fails_as_regular_user(self):
        """
        List Report as regular user.
        Response report-code should be 403 Forbidden because only admin can do it.
        """
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_list_report_report_succeeds_as_admin_user(self):
        """
        List Report as regular user.
        Response report-code should be 200 OK and the length should be the same between reponse and queryset.
        """
        self.set_user_admin_credential()
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_200_OK)

        report_qs = Report.objects.all()
        report_qs_page_1 = Paginator(report_qs, 1)
        eq_(response.data.get('count'), report_qs_page_1.count)


class TestReportDetailTestCase(TestReportBaseClass):
    """
    Tests /report detail operations.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Before TestCase is run, set some data.
        """
        return super().setUpTestData(cls)

    def get_request_with_data(self, url):
        """
        Send POST request with data to defined URL.
        """
        response = self.client.get(url, format='json')
        return response

    def test_retrieve_self_report_succeeds(self):
        """
        Retrieve self Report details.
        Response status-code should be 200 OK.
        """
        url = reverse('report-detail', kwargs={'pk': self.report_3.id})
        response = self.get_request_with_data(url)

        eq_(response.status_code, http_status.HTTP_200_OK)
