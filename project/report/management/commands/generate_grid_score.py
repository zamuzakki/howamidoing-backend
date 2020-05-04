__author__ = 'zakki@kartoza.com'

from project.report.models import KmGrid, KmGridScore, Report
from django.core.management.base import BaseCommand

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Base command to generate KmGridScore from KmGrid and Report
    """
    def handle(self, **options):
        generate_grid_score()

def generate_grid_score():
    """
    Generate KmGridScore from KmGrid and Report
    """

    # Query all grids
    grids = KmGrid.objects.all()

    # Loop each grid
    for grid in grids:
        # Query reports contained within each grid
        grid_report = Report.objects.location_within(grid.geometry).order_by(
            'user', '-id'
        ).distinct('user')
        green_report = grid_report.green_report()
        yellow_report = grid_report.yellow_report()
        red_report = grid_report.red_report()

        # Create KmGridScore object
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
