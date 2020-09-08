from django.conf  import settings
from nose.tools import eq_
from rest_framework.test import APITestCase
from faker import Faker

from project.report.management.commands.import_grid import read_local_file, check_json_loadable, \
    check_geojson_loadable


fake = Faker()

class TestKmGridScoreVectorTile(APITestCase):
    """
    Test the endpoint of KmGridScore that serves vector tile
    """

    def setUp(self) -> None:
        self.url = '/v2/api/grid-score-tiles/?tile={}/{}/{}'

        # import KmGrid
        _, geojson = check_geojson_loadable(
            check_json_loadable(
                read_local_file(f'{settings.BASE_DIR}/../example/grid.geojson')
            )[1]
        )

    def test_mvt_not_found(self):
        """
        In this zoom, x, and y value, the endpoint should not return
        vector tile and the status code must be 204
        """
        response = self.client.get(self.url.format(14, 2000, 2000))
        eq_(response.status_code, 204)