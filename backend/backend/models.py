from django.db import models

class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(null=True, blank=True)

    # To generate a single table
    class Meta:
        abstract = True
