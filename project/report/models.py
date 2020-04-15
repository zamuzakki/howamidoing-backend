from django.contrib.gis.db import models as gis
from django.db import models
from project.users.models import User


class Status(models.Model):
    """
    Model for status used in report.
    """
    name = models.CharField(max_length=50, null=False, blank=False, default='')
    description = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return '{} | {}'.format(self.id, self.name)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Statuses'

class Report(models.Model):
    """
    Model representing report about latest User status
    """
    location = gis.PointField(null=True, default=None, blank=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=False, blank=False, default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, blank=False, default=1)

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.id, self.location, self.timestamp, self.user.username)

    class Meta:
        ordering = ('-id',)

class KmGrid(models.Model):
    """
    Model representing population number in certain grid
    """
    geometry = gis.PolygonField(null=True, blank=True, default=None)
    population = models.IntegerField(null=False, blank=False, default=300)

    def __str__(self):
        return '{} | {} | {}'.format(self.id, self.geometry, self.population)

    class Meta:
        # Temporarily set managed to False because we still don't know
        # how to create the data
        managed = False
        ordering = ('-id',)

class KmGridScore(models.Model):
    """
    Model representing Materialized Views for User status summary per grid
    """
    geometry = gis.PolygonField(null=True, blank=True, default=None)
    score_1 = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, default=0)
    score_2 = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, default=0)
    score_3 = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, default=0)
    population = models.IntegerField(null=False, blank=False, default=300)
    total_score = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False, default=0)

    def __str__(self):
        return '{} | {} | {} | {}'.format(self.id, self.geometry, self.population, self.total_score)

    class Meta:
        # Set managed to False because this model will access existing Materialized Views
        managed = False
        ordering = ('-id',)
