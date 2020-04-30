__author__ = 'zakki@kartoza.com'

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry
from project.report.models import KmGrid
import os
import json

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This script is for creating KmGrid object from GEOJSON file. \n' \
        'Usage: \n' \
        '--file /path/to/file/location/file.geojson'

    def add_arguments(self, parser):
        """ Define arguments for the command """
        parser.add_argument(
            '--file',
            dest='file',
            help='Location of GEOJSON file',
        )

    def handle(self, **options):
        """ Extracts options added to the command and returns appropriate data """
        try:
            if options['file']:
                file_loc = os.path.abspath(options['file'])

                print('Importing KmGrid from {}'.format(file_loc))
                print('Checking whether file exists')

                if check_path_exist_and_is_file(file_loc):
                    print('File exists!')
                    print('Check and load GEOJSON.')

                    content = read_local_file(file_loc)
                    is_json, json_data = check_json_loadable(content)
                    if is_json:
                        is_geojson, geojson_data = check_geojson_loadable(json_data)
                        if is_geojson:
                            print("Valid GEOJSON file! Inserting KmGrid.")
                            loop_geojson(geojson_data)
                        else:
                            print('File is not a GEOJSON file.')
                    else:
                        print('File is not a JSON file.')
                else:
                    print('File does not exist or path is not a file!')
                    print('Stopping import process.')

        except Exception as e:
            print(e)

def check_path_exist_and_is_file(file_path):
    return os.path.isfile(file_path)

def read_local_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
        return content

def check_json_loadable(string_json):
    try:
        json_data = json.loads(string_json)
    except Exception:
        return False, {}
    return True, json_data

def check_geojson_loadable(json_data):
    if all(field in ['name', 'type', 'crs', 'features'] for field in json_data.keys()):
        return True, json_data
    else:
        return False, json_data

def loop_geojson(geojson_data):
    for i, grid in enumerate(geojson_data['features']):
        create_single_grid_from_features(grid)

def create_single_grid_from_features(grid):
    geometry = GEOSGeometry(str(grid['geometry']))
    population = grid['properties']['population_count']
    grid = KmGrid.objects.create(
        geometry=geometry,
        population=population
    )
    grid.save()
    return grid
