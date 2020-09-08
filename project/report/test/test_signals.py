from nose.tools import eq_
from rest_framework.test import APITestCase
from faker import Faker

from project.report.models.report import Report
from project.report.models.km_grid_score import KmGridScore
from project.report.test.factories import (
    KmGridFactory,
    ReportFactory,
    StatusFactory,
    UserFactory,
    STATUS_NAME
)


fake = Faker()

class TestReportSignals(APITestCase):
    """
    TestCase for Report signals. When Report is created,
    it will recalculate score of the grid.
    """

    @classmethod
    def setUpTestData(self):
        """
        Setup initial testdata
        """

        # We set the population to 1 so it's easier for us
        # to track the score value.
        self.grid_1 = KmGridFactory.create(id=1, population=1)
        self.grid_2 = KmGridFactory.create(id=2, population=1)
        self.status_green = StatusFactory.create(id=1, name=STATUS_NAME[0], description=STATUS_NAME[0])
        self.status_yellow = StatusFactory.create(id=2, name=STATUS_NAME[1], description=STATUS_NAME[1])
        self.status_red = StatusFactory.create(id=3, name=STATUS_NAME[2], description=STATUS_NAME[2])
        self.user = UserFactory.create()

    # def test_first_report_green(self):
    #     """
    #     Test creating first Report for user. The status is 'All Well Here'.
    #     It should create a new KmGridScore object.
    #     """
    #     old_km_grid_score = KmGridScore.objects.all()
    #
    #     # The count of KmGridScore should be 0
    #     eq_(old_km_grid_score.count(), 0)
    #
    #     ReportFactory.create(
    #         grid=self.grid_1,
    #         status=self.status_green,
    #         user=self.user
    #     )
    #
    #     new_km_grid_score = KmGridScore.objects.all()
    #
    #     # The count of KmGridScore should be 1
    #     eq_(new_km_grid_score.count(), 1)
    #
    #     km_grid_score = new_km_grid_score.get(geometry=self.grid_1.geometry)
    #     eq_(km_grid_score.count_green, 1)
    #     eq_(km_grid_score.score_green, 1)
    #     eq_(km_grid_score.count_yellow, 0)
    #     eq_(km_grid_score.score_yellow, 0)
    #     eq_(km_grid_score.count_red, 0)
    #     eq_(km_grid_score.score_red, 0)
    #     eq_(km_grid_score.population, 1)
    #     eq_(int(km_grid_score.total_score), 0)
    #
    # def test_first_report_yellow(self):
    #     """
    #     Test creating first Report for user. The status is 'Need Food or Supplies'.
    #     It should create a new KmGridScore object.
    #     """
    #     old_km_grid_score = KmGridScore.objects.all()
    #
    #     # The count of KmGridScore should be 0
    #     eq_(old_km_grid_score.count(), 0)
    #
    #     ReportFactory.create(
    #         grid=self.grid_1,
    #         status=self.status_yellow,
    #         user=self.user
    #     )
    #
    #     new_km_grid_score = KmGridScore.objects.all()
    #
    #     # The count of KmGridScore should be 1
    #     eq_(new_km_grid_score.count(), 1)
    #
    #     km_grid_score = new_km_grid_score.get(geometry=self.grid_1.geometry)
    #     eq_(km_grid_score.count_green, 0)
    #     eq_(km_grid_score.score_green, 0)
    #     eq_(km_grid_score.count_yellow, 1)
    #     eq_(km_grid_score.score_yellow, 2)
    #     eq_(km_grid_score.count_red, 0)
    #     eq_(km_grid_score.score_red, 0)
    #     eq_(km_grid_score.population, 1)
    #     eq_(int(km_grid_score.total_score), 2)
    #
    # def test_first_report_red(self):
    #     """
    #     Test creating first Report for user. The status is 'Need Medical Help'.
    #     It should create a new KmGridScore object.
    #     """
    #     old_km_grid_score = KmGridScore.objects.all()
    #
    #     # The count of KmGridScore should be 0
    #     eq_(old_km_grid_score.count(), 0)
    #
    #     ReportFactory.create(
    #         grid=self.grid_1,
    #         status=self.status_red,
    #         user=self.user
    #     )
    #
    #     new_km_grid_score = KmGridScore.objects.all()
    #
    #     # The count of KmGridScore should be 1
    #     eq_(new_km_grid_score.count(), 1)
    #
    #     km_grid_score = new_km_grid_score.get(geometry=self.grid_1.geometry)
    #     eq_(km_grid_score.count_green, 0)
    #     eq_(km_grid_score.score_green, 0)
    #     eq_(km_grid_score.count_yellow, 0)
    #     eq_(km_grid_score.score_yellow, 0)
    #     eq_(km_grid_score.count_red, 1)
    #     eq_(km_grid_score.score_red, 5)
    #     eq_(km_grid_score.population, 1)
    #     eq_(int(km_grid_score.total_score), 2)
    #
    def test_second_report_same_grid(self):
        """
        Test creating second report when the user has previous report. The grid
        of those reports are same. The first report should be marked as old.
        Second report will recalculate first KmGridScore based on last report,
        instead of creating a new KmGridScore.
        """
        first_report = ReportFactory.create(
            grid=self.grid_1,
            status=self.status_green,
            user=self.user
        )
        # The first report must not be marked as old
        eq_(first_report.current, True)

        first_km_grid_scores = KmGridScore.objects.all()
        eq_(first_km_grid_scores.count(), 1)
        first_km_grid_score = first_km_grid_scores.get(geometry=first_report.grid.geometry)
        eq_(first_km_grid_score.count_green, 1)
        eq_(first_km_grid_score.count_red, 0)
        eq_(int(first_km_grid_score.total_score), 0)

        second_report = ReportFactory.create(
            grid=self.grid_1,
            status=self.status_red,
            user=self.user
        )
        first_report = Report.objects.get(id=first_report.id)

        # The first report must be marked as old
        self.assertFalse(first_report.current, False)
        self.assertTrue(second_report.current, True)
        eq_(Report.objects.all().count(), 2)

        second_km_grid_scores = KmGridScore.objects.all()
        # The count of KmGridScore is not changed
        eq_(second_km_grid_scores.count(), 1)
        second_km_grid_score = second_km_grid_scores.get(geometry=second_report.grid.geometry)

        # The property of the KmGridScore is changed
        eq_(second_km_grid_score.count_green, 0)
        eq_(second_km_grid_score.count_red, 1)
        eq_(int(second_km_grid_score.total_score), 2)

    def test_second_report_different_grid(self):
        """
        Test creating second report when the user has previous report. The grid
        of those reports are different. The first report should be marked as old.
        Second report will recalculate first and second KmGridScore based on last report
        """
        first_report = ReportFactory.create(
            grid=self.grid_1,
            status=self.status_green,
            user=self.user
        )

        first_km_grid_scores = KmGridScore.objects.all()
        eq_(first_km_grid_scores.count(), 1)
        first_km_grid_score = first_km_grid_scores.get(geometry=first_report.grid.geometry)
        eq_(first_km_grid_score.count_green, 1)
        eq_(first_km_grid_score.count_red, 0)
        eq_(int(first_km_grid_score.total_score), 0)

        second_report = ReportFactory.create(
            grid=self.grid_2,
            status=self.status_red,
            user=self.user
        )

        second_km_grid_scores = KmGridScore.objects.all()
        # The count of KmGridScore should be changed
        eq_(second_km_grid_scores.count(), 2)
        second_km_grid_score = second_km_grid_scores.get(geometry=second_report.grid.geometry)
        first_km_grid_score = second_km_grid_scores.get(id=first_km_grid_score.id)

        # The property of the first KmGridScore should be updated.
        # The count is now 0, because even if there is Report in this
        # grid, that Report marked as old report.
        eq_(first_km_grid_score.count_green, 0)
        eq_(first_km_grid_score.count_red, 0)
        eq_(int(first_km_grid_score.total_score), 0)

        # The second grid property must match the expected calculation
        eq_(second_km_grid_score.count_green, 0)
        eq_(second_km_grid_score.count_red, 1)
        eq_(int(second_km_grid_score.total_score), 2)
