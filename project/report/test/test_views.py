from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
from nose.tools import eq_, assert_not_equal
from rest_framework.test import APITestCase
from rest_framework import status as http_status
from faker import Faker
from project.report.models import Status, Report, KmGrid
from .factories import StatusFactory, ReportFactory
from project.users.test.factories import UserFactory, UserAdminFactory
from project.report.management.commands.import_grid import read_local_file, check_json_loadable, \
    check_geojson_loadable, create_single_grid_from_features
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

    def test_create_status_with_empty_data_fails_as_regular_user(self):
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
        cls.user_1 = UserFactory()
        cls.user_2 = UserFactory()
        cls.user_admin = UserAdminFactory()

        cls.status_1 = StatusFactory()
        cls.status_2 = StatusFactory()

        cls.report_1 = ReportFactory(user=cls.user_1)
        cls.report_2 = ReportFactory(user=cls.user_2)
        cls.report_admin = ReportFactory(user=cls.user_admin)

        cls.location_1 = cls.report_1.location
        cls.report_1_json = {
            "location": {
                "type": "Point",
                "coordinates": [
                    cls.location_1.x,
                    cls.location_1.y
                ]
            },
            "status": cls.status_1.id,
            "user": cls.user_1.id,
        }

        cls.location_2 = cls.report_2.location
        cls.report_2_json = {
            "location": {
                "type": "Point",
                "coordinates": [
                    cls.location_2.x,
                    cls.location_2.y
                ]
            },
            "status": cls.status_2.id,
            "user": cls.user_2.id,
        }

        cls.location_admin = cls.report_admin.location
        cls.report_admin_json = {
            "location": {
                "type": "Point",
                "coordinates": [
                    cls.location_admin.x,
                    cls.location_admin.y
                ]
            },
            "status": cls.status_1.id,
            "user": cls.user_admin.id,
        }

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

    def set_user_admin_credential(self):
        """
        Set user_admin credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_admin.auth_token}')


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

    def test_create_report_with_empty_data_fails_as_regular_user_1(self):
        """
        Create new Report using post request with empty data as regular user.
        Response status-code should be 403 Forbidden.
        """
        self.set_user_1_credential()
        response = self.post_request_with_data({})
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_create_self_report_with_valid_data_succeeds_as_regular_user(self):
        """
        Create new Report using post request with valid data as regular user.
        Response status-code should be 201 Created the length should be the same between reponse and queryset.
        """
        self.set_user_1_credential()
        response = self.post_request_with_data(self.report_1_json)
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        report = Report.objects.get(pk=response.data['id'])
        eq_(report.user.id, response.data['properties']['user'])
        eq_(report.status.id, response.data['properties']['status'])

    def test_create_report_with_valid_data_succeeds_as_admin_user(self):
        """
        Create new Report using post request with valid data as admin user.
        Response status-code should be 201 Created the length should be the same between reponse and queryset.
        """
        self.set_user_admin_credential()
        response = self.post_request_with_data(self.report_admin_json)
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        report = Report.objects.get(pk=response.data['id'])
        eq_(report.user.id, response.data['properties']['user'])
        eq_(report.status.id, response.data['properties']['status'])

    def test_list_report_fails_as_regular_user(self):
        """
        List Report as regular user.
        Response report-code should be 403 Forbidden because only admin can do it.
        """
        self.set_user_1_credential()
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

    def post_request_with_data(self, url, data):
        """
        Send POST request with data to defined URL.
        """
        response = self.client.post(url, data, format='json')
        return response

    def put_request_valid_data(self, url, data):
        """
        Send PUT request with data to defined URL.
        :returns response
        """
        response = self.client.put(url, data, format='json')
        return response

    def delete_request_valid_data(self, url):
        """
        Send DELETE request with data to defined URL.
        :return response data
        """
        response = self.client.delete(url)
        return response

    def test_retrieve_self_report_succeeds_as_admin_user(self):
        """
        Retrieve self Report details as admin user.
        Response status-code should be 200 OK.
        """
        self.set_user_admin_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_admin.id})
        response = self.get_request_with_data(url)

        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_retrieve_others_report_succeeds_as_admin_user(self):
        """
        Retrieve self Report details as admin user.
        Response status-code should be 200 OK.
        """
        self.set_user_admin_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_1.id})
        response = self.get_request_with_data(url)

        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_retrieve_self_report_succeeds_as_regular_user(self):
        """
        Retrieve self Report details as regular user.
        Response status-code should be 200 OK.
        """
        self.set_user_1_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_1.id})
        response = self.client.get(url, format='json')
        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_retrieve_others_report_succeeds_as_regular_user(self):
        """
        Retrieve others Report details as regular user.
        Response status-code should be 403 Forbidden.
        """
        self.set_user_1_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_2.id})
        response = self.get_request_with_data(url)
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_update_a_report_succeeds_as_admin_user(self):
        """
        Update Report details as admin user.
        Response status-code should be 200 OK and Report status and user should be updated.
        """
        self.set_user_admin_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_1.id})
        data = self.report_2_json

        response = self.put_request_valid_data(url, data)
        eq_(response.status_code, http_status.HTTP_200_OK)

        report = Report.objects.get(pk=self.report_1.id)
        eq_(report.status.id, response.data['properties']['status'])
        eq_(report.user.id, response.data['properties']['user'])

    def test_update_others_report_fails_as_regular_user(self):
        """
        Update Report details as regular user.
        Response status-code should be 403 Forbidden and Report name should not be updated
        """
        self.set_user_1_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_2.id})
        data = self.report_1_json

        response = self.put_request_valid_data(url, data)
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_delete_a_report_succeeds_as_admin_user(self):
        """
        Delete Report as admin user.
        Response status-code should be 204 No Content and Report be deleted.
        """
        self.set_user_admin_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_admin.id})
        response = self.client.delete(url)
        eq_(response.status_code, http_status.HTTP_204_NO_CONTENT)

        report = Report.objects.filter(id=self.report_admin.id)
        eq_(report.count(), 0)

    def test_delete_a_report_succeeds_as_regular_user(self):
        """
        Delete Report as regular user.
        Response status-code should be 403 Forbidden.
        """
        self.set_user_admin_credential()
        url = reverse('report-detail', kwargs={'pk': self.report_admin.id})
        response = self.client.delete(url)
        eq_(response.status_code, http_status.HTTP_204_NO_CONTENT)

        report = Report.objects.filter(id=self.report_admin.id)
        eq_(report.count(), 0)


class TestKmGridBaseClass(APITestCase):
    """
    Base Class for KmGrid test case.
    """

    def setUpTestData(cls):
        """
        Set base data for all test case
        """
        cls.user_1 = UserFactory()
        cls.user_admin = UserAdminFactory()

        _, cls.geojson = check_geojson_loadable(
            check_json_loadable(
                read_local_file(f'{settings.BASE_DIR}/../example/grid.geojson')
            )[1]
        )

        cls.grid_1_json = {
            "geometry": cls.geojson['features'][0]['geometry'],
            "population": cls.geojson['features'][0]['properties']['population_count']
        }

        cls.grid_2_json = {
            "geometry": cls.geojson['features'][1]['geometry'],
            "population": cls.geojson['features'][1]['properties']['population_count']
        }

        cls.grid_1 = create_single_grid_from_features(cls.geojson['features'][0])
        cls.grid_2 = create_single_grid_from_features(cls.geojson['features'][1])

    def set_user_1_credential(self):
        """
        Set user_1 credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')

    def set_user_admin_credential(self):
        """
        Set user_admin credential.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user_admin.auth_token}')


class TestKmGridListTestCase(TestKmGridBaseClass):
    """
    Tests /grid list operations.
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
        self.url = reverse('kmgrid-list')

    def post_request_with_data(self, data):
        """
        Send POST request with data to defined URL.
        """
        response = self.client.post(self.url, data, format='json')
        return response

    def test_create_grid_with_empty_data_fails_as_regular_user(self):
        """
        Create new KmGrid using post request with empty data as regular user.
        Response status-code should be 400 Bad Request.
        """
        self.set_user_1_credential()
        response = self.post_request_with_data({})
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_create_grid_with_empty_data_fails_as_admin_user(self):
        """
        Create new KmGrid using post request with empty data as admin user.
        Response status-code should be 400 Bad Request.
        """
        self.set_user_admin_credential()
        response = self.post_request_with_data({})
        eq_(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_create_grid_with_valid_data_fails_as_regular_user(self):
        """
        Create new KmGrid using post request with valid data as regular user.
        Response status-code should be 403 Forbidden since only admin can do it.
        """
        self.set_user_1_credential()
        response = self.post_request_with_data(self.geojson)
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_create_grid_with_valid_data_succeeds_as_admin_user(self):
        """
        Create new KmGrid using post request with valid data as admin user.
        Response status-code should be 201 Created the length should be the same between reponse and queryset.
        """
        self.set_user_admin_credential()
        response = self.post_request_with_data(self.grid_1_json)
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        grid = KmGrid.objects.get(pk=response.data['id'])
        eq_(grid.population, response.data['properties']['population'])

    def test_list_grid_succeeds_as_regular_user(self):
        """
        List KmGrid as regular user.
        Response grid-code should be 200 OK.
        """
        self.set_user_1_credential()
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_list_grid_grid_succeeds_as_admin_user(self):
        """
        List KmGrid as regular user.
        Response grid-code should be 200 OK and the length should be the same between reponse and queryset.
        """
        self.set_user_admin_credential()
        response = self.client.get(self.url, {'page': 1})
        eq_(response.status_code, http_status.HTTP_200_OK)

        grid_qs = KmGrid.objects.all()
        grid_qs_page_1 = Paginator(grid_qs, 1)
        eq_(response.data.get('count'), grid_qs_page_1.count)

class TestKmGridDetailTestCase(TestKmGridBaseClass):
    """
    Tests /grid detail operations.
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

    def post_request_with_data(self, url, data):
        """
        Send POST request with data to defined URL.
        """
        response = self.client.post(url, data, format='json')
        return response

    def put_request_valid_data(self, url, data):
        """
        Send PUT request with data to defined URL.
        :returns response
        """
        response = self.client.put(url, data, format='json')
        return response

    def delete_request_valid_data(self, url):
        """
        Send DELETE request with data to defined URL.
        :return response data
        """
        response = self.client.delete(url)
        return response

    def test_retrieve_grid_succeeds_as_admin_user(self):
        """
        Retrieve self KmGrid details as admin user.
        Response status-code should be 200 OK.
        """
        self.set_user_admin_credential()
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_1.id})
        response = self.get_request_with_data(url)

        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_retrieve_grid_succeeds_as_regular_user(self):
        """
        Retrieve self KmGrid details as regular user.
        Response status-code should be 200 OK.
        """
        self.set_user_1_credential()
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_1.id})
        response = self.client.get(url, format='json')
        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_update_a_grid_succeeds_as_admin_user(self):
        """
        Update KmGrid details as admin user.
        Response status-code should be 200 OK and KmGrid status and user should be updated.
        """
        self.set_user_admin_credential()
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_1.id})
        data = self.grid_2_json

        response = self.put_request_valid_data(url, data)
        eq_(response.status_code, http_status.HTTP_200_OK)

        grid = KmGrid.objects.get(pk=self.grid_1.id)
        eq_(grid.population, response.data['properties']['population'])

    def test_update_others_grid_fails_as_regular_user(self):
        """
        Update KmGrid details as regular user.
        Response status-code should be 403 Forbidden
        """
        self.set_user_1_credential()
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_2.id})
        data = self.grid_1_json

        response = self.put_request_valid_data(url, data)
        eq_(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_delete_a_grid_succeeds_as_admin_user(self):
        """
        Delete KmGrid as admin user.
        Response status-code should be 204 No Content and KmGrid be deleted.
        """
        self.set_user_admin_credential()
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_1.id})
        response = self.client.delete(url)
        eq_(response.status_code, http_status.HTTP_204_NO_CONTENT)

        grid = KmGrid.objects.filter(id=self.grid_1.id)
        eq_(grid.count(), 0)

    def test_delete_a_grid_succeeds_as_regular_user(self):
        """
        Delete KmGrid as regular user.
        Response status-code should be 403 Forbidden.
        """
        self.set_user_admin_credential()
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_1.id})
        response = self.client.delete(url)
        eq_(response.status_code, http_status.HTTP_204_NO_CONTENT)

        grid = KmGrid.objects.filter(id=self.grid_1.id)
        eq_(grid.count(), 0)
