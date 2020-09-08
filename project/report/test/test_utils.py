from django.test import TestCase
from nose.tools import eq_
from project.report.utils.scoring_grid import color_score_km_grid, status_score_km_grid


class TestScoringGrid(TestCase):
    """
    TestCase for ScoringGrid
    """

    @classmethod
    def setUpTestData(cls):
        """
        setup test data
        """
        cls.population_1 = 100
        cls.population_2 = 60
        cls.count_red = 8
        cls.count_yellow = 14
        cls.count_green = 30

    def test_score_red(self):
        """
        Test score for red status
        """
        score = color_score_km_grid(self.count_red, self.population_1, 'red')
        eq_(score, 0.4)

    def test_score_yellow(self):
        """
        Test score for yellow status
        """
        score = color_score_km_grid(self.count_yellow, self.population_1, 'yellow')
        eq_(score, 0.28)

    def test_score_green(self):
        """
        Test score for green status
        """
        score = color_score_km_grid(self.count_green, self.population_1, 'green')
        eq_(score, 0.3)

    def test_score_total_with_higher_population(self):
        """
        Test total score for higher number of population
        """
        score = status_score_km_grid(
            self.count_green,
            self.count_yellow,
            self.count_red,
            self.population_1
        )
        eq_(score, 2)

    def test_score_total_with_lower_population(self):
        """
        Test total score for lower number of population
        """
        score = status_score_km_grid(
            self.count_green,
            self.count_yellow,
            self.count_red,
            self.population_2
        )
        eq_(score, 2)
