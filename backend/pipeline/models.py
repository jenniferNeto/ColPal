from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    is_stable = models.BooleanField(default=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    hard_deadline = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        abstract = True

class Pipeline(Pipe):
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    def save(self, *args, **kwargs):
        # Update the last_modification timestamp
        self.last_modified = datetime.now(tz=timezone.get_current_timezone())

        super().save(*args, **kwargs)

        # Update approved date when pipeline is approved
        if self.is_approved and not self.approved_date:
            self.approved_date = timezone.now()

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

class PipelineNotification(models.Model):
    """Represents notification requests for pipelines"""
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date = models.DateTimeField(default=timezone.now, null=False)
    title = models.TextField(null=False)
    message = models.TextField(null=False)
