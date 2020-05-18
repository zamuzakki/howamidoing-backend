from django.db import models
from django.utils.translation import ugettext_lazy as _
import logging

logger = logging.getLogger(__name__)


class Status(models.Model):
    """
    Status used in report, e.g. 'All Well Here', 'We Need Medical Help', etc.
    """
    name = models.CharField(
        help_text=_('Name of this status'),
        max_length=50,
        null=False,
        blank=False,
        default=''
    )

    description = models.TextField(
        help_text=_('Brief description of this status'),
        null=True,
        blank=True,
        default=None
    )

    def __str__(self):
        return '{} | {}'.format(self.id, self.name)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Statuses'
