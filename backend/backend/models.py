from django.db import models
from datetime import datetime

class TimeStamp(models.Model):
    created = models.DateTimeField(default=datetime.now)
    last_modified = models.DateTimeField(null=True, blank=True)

    # To generate a single table
    class Meta:
        abstract = True
