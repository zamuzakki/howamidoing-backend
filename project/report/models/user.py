from django.db import models
import uuid
import logging

logger = logging.getLogger(__name__)


class User(models.Model):
    """
    User/owner of the Report
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return '{}'.format(self.id)
