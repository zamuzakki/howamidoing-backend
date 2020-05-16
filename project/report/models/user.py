from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
import logging

logger = logging.getLogger(__name__)


class User(models.Model):
    """
    User/owner of the Report
    """
    id = models.UUIDField(
        help_text=_('UUID of the User'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    timestamp = models.DateTimeField(
        help_text=_('Timestamp of User creation'),
        auto_now_add=True
    )

    def __str__(self):
        return '{}'.format(self.id)

    class Meta:
        ordering = ('-timestamp',)
