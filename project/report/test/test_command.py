from contextlib import redirect_stdout
from django.conf import settings
from nose.tools import eq_
from rest_framework.test import APITestCase
from rest_framework import status as http_status
from faker import Faker
from project.report.models.km_grid import KmGrid
from project.users.test.factories import UserAdminFactory
from project.report.management.commands.import_grid import read_local_file, check_json_loadable, \
    check_geojson_loadable, check_path_exist_and_is_file, import_grid_from_geojson
from project.report.management.commands.generate_grid_score import generate_grid_score
import io
import json

fake = Faker()

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


class TestGenerateKmGridScore(APITestCase):
    """
    TestCase for KmGrid import using command and admin page
    """

    @classmethod
    def setUpTestData(self):
        """
        Setup initial testdata
        """
        self.valid_file_path = f'{settings.BASE_DIR}/../example/grid.geojson'

    def test_generate_grid_score(self):
        """
        Test command to generate KmGridScore from KmGrid.
        """
        f = io.StringIO()
        with redirect_stdout(f):
            import_grid_from_geojson(self.valid_file_path)
        output = f.getvalue()
        before, keyword, after = output.partition('Imported ')
        imported_grids = int(after.split('/')[0])

        with redirect_stdout(f):
            generate_grid_score()
        output = f.getvalue()
        before, keyword, after = output.partition(' Grid Scores Inserted --')
        generated_grid_score = int(before.split('-- ')[-1])

        eq_(imported_grids, generated_grid_score)
