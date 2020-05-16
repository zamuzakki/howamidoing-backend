from contextlib import redirect_stdout
from django.urls import reverse
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
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
from .factories import StatusFactory, ReportFactory, UserFactory, KmGridFactory
from project.users.test.factories import UserAdminFactory
from project.report.management.commands.import_grid import read_local_file, check_json_loadable, \
    check_geojson_loadable, check_path_exist_and_is_file, \
    import_grid_from_geojson
import factory
import io
import json

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
        Response status-code should be 200 OK and the length should be the same between reponse and queryset.
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
        cls.user_2 = UserFactory()
        cls.user_admin = UserAdminFactory()

        cls.status_1 = StatusFactory()
        cls.status_2 = StatusFactory()

        cls.report_1 = ReportFactory(user=cls.user_1)
        cls.report_2 = ReportFactory(user=cls.user_2)

        cls.grid_1 = cls.report_1.grid
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

        cls.grid_2 = cls.report_2.grid
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
            "user": cls.user_2.id,
        }

    def set_user_admin_credential(self):
        """
        Set admin user credential.
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
        Response status-code should be 500 Internal Server Error.
        """
        response = self.post_request_with_data({})
        eq_(response.status_code, http_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_create_self_report_with_valid_data_succeeds_as_regular_user(self):
        """
        Create new Report using post request with valid data as regular user.
        Response status-code should be 201 Created the length should be the same between reponse and queryset.
        """
        response = self.post_request_with_data(self.report_1_json)
        eq_(response.status_code, http_status.HTTP_201_CREATED)

        report = Report.objects.get(pk=response.data['id'])
        eq_(report.user.id, response.data['user'])
        eq_(report.status.id, response.data['status'])

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

    def post_request_with_data(self, url, data):
        """
        Send POST request with data to defined URL.
        """
        response = self.client.post(url, data, format='json')
        return response

    def test_retrieve_self_report_succeeds(self):
        """
        Retrieve self Report details.
        Response status-code should be 200 OK.
        """
        url = reverse('report-detail', kwargs={'pk': self.report_1.id})
        response = self.get_request_with_data(url)

        eq_(response.status_code, http_status.HTTP_200_OK)


class TestKmGridBaseClass(APITestCase):
    """
    Base Class for KmGrid test case.
    """

    def setUpTestData(cls):
        """
        Set base data for all test case
        """
        cls.user_admin = UserAdminFactory()

        cls.grid_1 = KmGridFactory()
        cls.centroid_1 = KmGrid.objects.filter(id=cls.grid_1.id).\
            annotate(centroid=Centroid('geometry'))[0].centroid
        cls.grid_2 = KmGridFactory()
        cls.centroid_2 = KmGrid.objects.filter(id=cls.grid_2.id).\
            annotate(centroid=Centroid('geometry'))[0].centroid

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

    def test_list_grid_succeeds_as_regular_user(self):
        """
        List KmGrid as regular user.
        Response grid-code should be 200 OK.
        """
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

    def test_filter_grid_with_parameter_succeeds_as_regular_user(self):
        """
        Filter KmGrid with parameter as regular user.
        Response grid-code should be 200 OK and showing filtered results.
        """
        params = {
            "max_population": 100,
            "min_population": 90,
            "contains_geom": {
                "type": "Point",
                "coordinates": [
                    self.centroid_1.x,
                    self.centroid_1.y
                ]
            }
        }
        param = f"?max_population={params['max_population']}&" + \
            f"min_population={params['min_population']}&" + \
            f"contains_geom={json.dumps(params['contains_geom'])}"

        response = self.client.get(self.url + param)
        eq_(response.status_code, http_status.HTTP_200_OK)

        filtered_grid = KmGrid.objects.filter(
            population__gte=params['min_population'],
            population__lte=params['max_population'],
            geometry__contains=GEOSGeometry(
                json.dumps(params['contains_geom']),
            )
        )
        eq_(response.data['count'], filtered_grid.count())


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

    def test_retrieve_grid_succeeds_as_admin_user(self):
        """
        Retrieve self KmGrid details as admin user.
        Response status-code should be 200 OK.
        """
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_1.id})
        response = self.get_request_with_data(url)

        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_retrieve_grid_succeeds_as_regular_user(self):
        """
        Retrieve self KmGrid details as regular user.
        Response status-code should be 200 OK.
        """
        url = reverse('kmgrid-detail', kwargs={'pk': self.grid_1.id})
        response = self.client.get(url, format='json')
        eq_(response.status_code, http_status.HTTP_200_OK)


class TestKmGridImport(APITestCase):
    """
    TestCase for KmGrid import using command and admin page
    """

    @classmethod
    def setUpTestData(self):
        """
        Setup initial testdata
        """
        self.admin = UserAdminFactory
        self.valid_file_path = f'{settings.BASE_DIR}/../example/grid.geojson'
        self.invalid_file_path = f'{settings.BASE_DIR}/../example/grid.json'
        self.valid_dir_path = f'{settings.BASE_DIR}/../example'
        self.invalid_dir_path = f'{settings.BASE_DIR}/../examples'
        self.valid_path_invalid_json = f'{settings.BASE_DIR}/../requirements.txt'

        self.valid_geojson = {
            "name": "grid",
            "crs": {
                "type": "name",
                "properties": {
                    "name": "urn:ogc:def:crs:OGC:1.3:CRS84"
                }
            },
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "population_count": 90.0
                    },
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
                    }
                }
            ]
        }
        self.valid_json_invalid_geojson = {
            "name": "grid",
            "type": "FeatureCollection"
        }
        self.valid_geojson_string = json.dumps(self.valid_geojson)
        self.valid_json_invalid_geojson_string = json.dumps(self.valid_json_invalid_geojson)
        self.invalid_json_string = "It is not valid"

    def login(self):
        """
        Method for login
        """
        self.client.login(email=self.admin.email, password=self.admin.password)

    def test_valid_file_path(self):
        """
        Test check_path_exist_and_is_file function.
        Should return True if path exists and is a file.
        Expected True because the path used to test exists and is a file.
        """
        eq_(check_path_exist_and_is_file(self.valid_file_path), True)

    def test_invalid_file_path(self):
        """
        Test check_path_exist_and_is_file function.
        Should return True if path exists and is a file.
        Expected False because the path used to test does not exist.
        """
        eq_(check_path_exist_and_is_file(self.invalid_file_path), False)

    def test_valid_directory_path(self):
        """
        Test check_path_exist_and_is_file function.
        Should return True if path exists and is a file.
        Expected False because the path used to test exists but it is not a file.
        """
        eq_(check_path_exist_and_is_file(self.invalid_file_path), False)

    def test_invalid_directory_path(self):
        """
        Test check_path_exist_and_is_file function.
        Should return True if path exists and is a file.
        Expected False because the path used to test does not exist and is not a file.
        """
        eq_(check_path_exist_and_is_file(self.invalid_file_path), False)

    def test_valid_json_string(self):
        """
        Test check_json_loadable function.
        Should return (True, parsed_data) if the string can be parsed to JSON.
        Expected (True, parsed_data) because the the test string is JSON parsable.
        """
        eq_(check_json_loadable(self.valid_geojson_string)[0], True)
        eq_(check_json_loadable(self.valid_geojson_string)[1], self.valid_geojson)
        eq_(check_json_loadable(self.valid_json_invalid_geojson_string)[0], True)
        eq_(check_json_loadable(self.valid_json_invalid_geojson_string)[1], self.valid_json_invalid_geojson)

    def test_invalid_json_string(self):
        """
        Test check_json_loadable function.
        Should return (True, parsed_data) if the string can be parsed to JSON.
        Expected (False, {}) because the the test string is not JSON parsable.
        """
        is_json, parsed_data = check_json_loadable(self.invalid_json_string)
        eq_(is_json, False)
        eq_(parsed_data, {})

    def test_valid_geojson(self):
        """
        Test check_geojson_loadable function.
        Should return (True, parsed_data) if the JSON is a GeoJSON.
        Expected (True, parsed_data) because the the test JSON is a GeoJSON.
        """
        eq_(check_geojson_loadable(self.valid_geojson)[0], True)

    def test_invalid_geojson(self):
        """
        Test check_geojson_loadable function.
        Should return (True, parsed_data) if the JSON is a GeoJSON.
        Expected (False, parsed_data) because the the test JSON is not a GeoJSON.
        """
        eq_(check_geojson_loadable(self.valid_json_invalid_geojson)[0], True)

    def test_import_grid_from_invalid_path(self):
        """
        Test import_grid_from_geojson function using invalid path.
        Expected 'File does not exist or path is not a file!' in the console output.
        """
        f = io.StringIO()
        with redirect_stdout(f):
            import_grid_from_geojson(self.invalid_file_path)
        output = f.getvalue()
        message = 'File does not exist or path is not a file!'
        eq_(message in output, True)

    def test_import_grid_from_valid_path_invalid_json(self):
        """
        Test import_grid_from_geojson function using valid path but invalid JSON.
        Expected 'File is not a JSON file.' in the console output.
        """
        f = io.StringIO()
        with redirect_stdout(f):
            import_grid_from_geojson(self.valid_path_invalid_json)
        output = f.getvalue()
        message = 'File is not a JSON file.'
        eq_(message in output, True)

    def test_import_grid_from_valid_path_valid_geojson(self):
        """
        Test import_grid_from_geojson function using valid path and valid GeoJSON.
        Expected 'Valid GEOJSON file! Inserting KmGrid.' in the console output and
            saved grid equals features length in GeoJSON.
        """
        f = io.StringIO()
        with redirect_stdout(f):
            import_grid_from_geojson(self.valid_file_path)
        output = f.getvalue()
        message = 'Valid GEOJSON file! Inserting KmGrid.'
        eq_(message in output, True)

        grid_count = KmGrid.objects.count()
        _, geojson = check_geojson_loadable(
            check_json_loadable(
                read_local_file(f'{settings.BASE_DIR}/../example/grid.geojson')
            )[1]
        )
        eq_(grid_count, len(geojson['features']))

    def test_url_to_import_kmgrid_can_be_opened(self):
        """
        Test Import KmGrid page can be opened in admin page.
        """
        self.login()
        response = self.client.get('/admin/report/kmgrid/import-geojson/', follow=True)
        eq_(response.status_code, http_status.HTTP_200_OK)

    def test_url_to_import_kmgrid_function_valid_file(self):
        """
        Test Import KmGrid function using correct GeoJSON file.
        """
        self.login()
        with open(self.valid_file_path) as fp:
            response = self.client.post(
                '/admin/report/kmgrid/import-geojson/',
                {'file': fp},
                follow=True
            )
            eq_(response.status_code, http_status.HTTP_200_OK)
            self.assertContains(response, 'Your GEOJSON file has been imported')

            grid_count = KmGrid.objects.count()
            _, geojson = check_geojson_loadable(
                check_json_loadable(
                    read_local_file(f'{settings.BASE_DIR}/../example/grid.geojson')
                )[1]
            )
            eq_(grid_count, len(geojson['features']))

    def test_url_to_import_kmgrid_function_invalid_file(self):
        """
        Test Import KmGrid function using non JSON file.
        """
        self.login()
        with open(self.valid_path_invalid_json) as fp:
            response = self.client.post(
                '/admin/report/kmgrid/import-geojson/',
                {'file': fp},
                follow=True
            )
            eq_(response.status_code, http_status.HTTP_200_OK)
            self.assertContains(response, 'File is not a JSON file.')
