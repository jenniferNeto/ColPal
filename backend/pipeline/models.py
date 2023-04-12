from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

from simple_history.models import HistoricalRecords

from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

from constraints.models import Constraint


class TimeStamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(null=True, blank=True)

    # To generate a single table
    class Meta:
        abstract = True

class Pipe(TimeStamp):
    title = models.CharField(max_length=40)
    upload_frequency = models.DurationField(default=timedelta)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    approved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        abstract = True

class Pipeline(Pipe):
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
            self.last_modified = datetime.now(tz=timezone.get_current_timezone())

        # If the pipeline is now approved update timestamp
        if self.is_approved and self.old_is_approved != self.is_approved:
            self.approved_date = datetime.now(tz=timezone.get_current_timezone())

        # Reset the approval date to null if the pipeline isn't approved anymore
        if not self.is_approved:
            self.approved_date = None

        super().save(*args, **kwargs)

    def save_without_historical_model(self, *args, **kwargs):
        """Copied from the documentation"""
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

class PipelineFile(models.Model):
    """Allows users to upload files to specific"""
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=False)
    file = models.FileField(storage=storage)
    path = models.FilePathField(null=True)
    upload_date = models.DateTimeField(default=timezone.now)
    template_file = models.BooleanField(default=False)

    def is_template(self):
        """Determine if a file is a template file"""
        line_count = 0

        # Instead of reading the entire file and returning line count
        # Just check to see if there's more than one line and return O(n) -> O(1)
        for _ in self.file.open('r'):
            line_count += 1

            if line_count > 1:
                return False
        return True

    def save(self, *args, **kwargs):
        # Mark file as a template file if it only includes headers
        # Need to do this before saving the object or it won't update
        self.template_file = self.is_template()

        # Need to save the object before creating constraints
        saved_object = super().save(*args, **kwargs)

        if self.template_file:
            # Open the uploaded file in read mode
            file = self.file.open('r')

            # Get all column names and strip special characters
            # Can split using comma as files will be csv
            columns = file.readline().decode("UTF-8").strip().split(",")

            # Create new default constraint objects
            for column in columns:
                Constraint.objects.create(pipeline=self.pipeline, column_title=column)
        return saved_object
