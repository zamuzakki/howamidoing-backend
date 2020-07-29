__author__ = 'zakki@kartoza.com'

from project.report.models.km_grid import KmGrid
from project.report.models.km_grid_score import KmGridScore
from project.report.models.report import Report
from django.core.management.base import BaseCommand

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Base command to generate KmGridScore from KmGrid and Report
    """
    def add_arguments(self, parser):
        """ Define arguments for the command """
        parser.add_argument(
            '--select',
            dest='select',
            help='Mode of KmGridScore generation',
        )
        parser.add_argument(
            '--grids',
            dest='grids',
            help='ID of KmGridScore, separated by comma',
        )

    def handle(self, **options):
        try:
            if options['select']:
                generate_grid_score(select=options['select'])

            if options['grids']:
                generate_grid_score(grids=options['grids'])

        except KeyError:
            generate_grid_score()

def generate_grid_score(select='all', grids=None):
    """
    Generate KmGridScore from KmGrid and Report
    """

    # We only generate KmGridScore for grid that's still not in KmGridScore
    # Query all grids
    if select == 'non-existing':
        # Query all grid score
        grid_score = KmGridScore.objects.all().values('geometry')
        grid_qs = KmGrid.objects.exclude(geometry__in=grid_score)
    elif select == 'all':
        grid_qs = KmGrid.objects.all()
    else:
        raise ValueError('select value must be "all" or "non-existing"')

    if grids is not None:
        grids = grids.split(',')
        grid_qs = KmGrid.objects.filter(id__in=grids)

    print(f'--- Inserting {grid_qs.count()} Grid Scores ---')

    # Loop each grid
    for num, grid in enumerate(grid_qs):
        # Query reports contained within each grid
        grid_report = Report.current_objects.filter(grid=grid, current=True)
        green_report = grid_report.green_report()
        yellow_report = grid_report.yellow_report()
        red_report = grid_report.red_report()

        # Create/Update KmGridScore object
        grid_score, _ = KmGridScore.objects.get_or_create(geometry=grid.geometry)
        grid_score.population = grid.population
        grid_score.count_green = green_report.count()
        grid_score.count_yellow = yellow_report.count()
        grid_score.count_red = red_report.count()
        grid_score.total_report = green_report.count() + yellow_report.count() + red_report.count()
        grid_score.save()

        grid_score.set_color_score('green')
        grid_score.set_color_score('yellow')
        grid_score.set_color_score('red')
        grid_score.set_total_score()

        if num % 50 == 0 and num > 0:
            print(f'{num} Grid Scores Inserted ')

    print(f'-- {grid_qs.count()} Grid Scores Inserted --')