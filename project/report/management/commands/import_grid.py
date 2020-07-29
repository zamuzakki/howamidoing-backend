__author__ = 'zakki@kartoza.com'

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import GEOSGeometry, Polygon
from project.report.models.km_grid import KmGrid
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
        """
        Extracts options added to the command
        Run import function to import Grid
        """
        try:
            if options['file']:
                file_loc = os.path.abspath(options['file'])
                import_grid_from_geojson(file_loc)

        except Exception as e:
            print(e)

def import_grid_from_geojson(file_path):
    print('Importing KmGrid from {}'.format(file_path))
    print('Checking whether file exists')

    if check_path_exist_and_is_file(file_path):
        print('File exists!')
        print('Check and load GEOJSON.')

        content = read_local_file(file_path)
        is_json, json_data = check_json_loadable(content)
        if is_json:
            is_geojson, geojson_data = check_geojson_loadable(json_data)
            if is_geojson:
                print("Valid GEOJSON file! Inserting KmGrid.")
                result = loop_geojson(geojson_data)
                print('Imported {}/{} ({})'.format(
                    result[0],
                    result[1],
                    (result[0]/result[1])/100
                )
                )
            else:
                print('File is not a GEOJSON file.')
        else:
            print('File is not a JSON file.')
    else:
        print('File does not exist or path is not a file!')
        print('Stopping import process.')


def check_path_exist_and_is_file(file_path):
    """
    Check if path exists and is file.
    ::params::
    file_path : path to be checked
    ::params type::
    file_path : string
    ::return ::
    True : if path exists and is file
    False : if path does not exists or is not a file
    ::return type :: boolean
    """
    return os.path.isfile(file_path)

def read_local_file(file_path):
    """
    Read local file.
    ::params::
    file_path : path of the to read
    ::params type::
    file_path : string
    ::return ::
    content of the file
    ::return type :: string
    """
    with open(file_path, 'r') as f:
        content = f.read()
        return content

def check_json_loadable(string_json):
    """
    Check if a string can be parsed to JSON.
    ::params::
    string_json : JSON string to check
    ::params type::
    string_json : string
    ::return :: (JSON loadable, parsed JSON)
    (False, {}) if the string is not JSON loadable
    (True, parsed_json_data) if the string is JSON loadable
    ::return type :: (boolean, dict)
    """
    try:
        json_data = json.loads(string_json)
    except Exception:
        return False, {}
    return True, json_data

def check_geojson_loadable(json_data):
    """
    Check if a JSON is a GeoJSON.
    The data should contain keys:
        name, type, crs,features
    ::params::
    json_data : JSON/dict to check
    ::params type::
    string_json : dict
    ::return :: (GeoJSON loadable, json_data)
    (False, json_data) if the dict is not a GeoJSON
    (True, json_data) if the dict is a GeoJSON
    ::return type :: (boolean, dict)
    """
    if type(json_data) != dict:
        return False, json_data
    elif all(field in ['type', 'features', 'name', 'crs'] for field in json_data.keys()):
        return True, json_data
    else:
        return False, json_data

def loop_geojson(geojson_data):
    """
    Loop GeoJSON and call function to create grid
    """
    created_object = 0
    to_import = len(geojson_data['features'])
    for idx, grid in enumerate(geojson_data['features']):
        grid = create_single_grid_from_features(grid, geojson_data['crs'])
        if grid is not None:
            created_object += 1
        if created_object % 100 == 0 and created_object > 0:
            print('{}/{} Grid Scores Inserted'.format(
                created_object,
                to_import
            ))

    return(created_object, len(geojson_data['features']))

def create_single_grid_from_features(grid, crs):
    """
    Create single grid based on single GeoJSON object
    """
    geom = Polygon((
        (grid['geometry']['coordinates'][0][0][0], grid['geometry']['coordinates'][0][0][1]),
        (grid['geometry']['coordinates'][0][1][0], grid['geometry']['coordinates'][0][1][1]),
        (grid['geometry']['coordinates'][0][2][0], grid['geometry']['coordinates'][0][2][1]),
        (grid['geometry']['coordinates'][0][3][0], grid['geometry']['coordinates'][0][3][1]),
        (grid['geometry']['coordinates'][0][4][0], grid['geometry']['coordinates'][0][4][1]),
    ), srid=3857)

    try:
        population = grid['properties']['population_count']
        if population == 0:
            population = 1
    except KeyError as e:
        print(e)
        return None

    try:
        grid = KmGrid.objects.create(
            geometry=geom,
            population=population
        )
        grid.save()
    except Exception as e:
        print(e)
        return None

    return grid