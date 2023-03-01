from django.db import models
from datetime import datetime, timedelta

from backend.models import TimeStamp


class Pipeline(TimeStamp):
    title = models.CharField(max_length=40)
    upload_frequency = models.DurationField(default=timedelta)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    approved_date = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Pipeline, self).__init__(*args, **kwargs)
        # Store defaults to check modification times
        self.old_title = self.title
        self.old_is_approved = self.is_approved
        self.old_upload_frequency = self.upload_frequency
        self.old_is_active = self.is_active

    def save(self, *args, **kwargs):
        # Update the last_modification timestamp
        if self.old_title != self.title or \
                self.old_is_approved != self.is_approved or \
                self.old_upload_frequency != self.upload_frequency or \
                self.old_is_active != self.is_active:
            self.last_modified = datetime.now()

        # If the pipeline is now approved update timestamp
        if self.is_approved and self.old_is_approved != self.is_approved:
            self.approved_date = datetime.now()

        # Reset the approval date to null if the pipeline isn't approved anymore
        if not self.is_approved:
            self.approved_date = None

        # Save the updated changes
        super(Pipeline, self).save(*args, **kwargs)

class ModificationPipelineRequest(Pipeline):
    class Meta:
        proxy = True
