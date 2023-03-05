from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
from simple_history.models import HistoricalRecords

from backend.models import TimeStamp

"""
TODO: Pipeline history should be storable and loadable.
Work on requesting pipeline changes and then on the history portion
Also USER settings needs to be the first thing set up


USER PERMISSION TO MAKE REQUESTS
PIPELINE HISTORY

"""

class Pipe(TimeStamp):
    title = models.CharField(max_length=40)
    upload_frequency = models.DurationField(default=timedelta)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    approved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.pk}, {self.title}'

    class Meta:
        abstract = True

class Pipeline(Pipe):
    history = HistoricalRecords(
        history_change_reason_field=models.TextField(null=True)
    )

    def createModificationPipeline(self, data):
        mod = Request.objects.create(title="Blank")
        print(data)

        mod.title = data['title']
        mod.upload_frequency = timedelta(0)
        mod.is_active = True if data['is_active'] == 'true' else False
        mod.update_reason = data['update_reason']
        mod.save()

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

class Request(Pipe):
    update_reason = models.TextField(null=True)

    changes_decisions = (
        (1, 'Accept'),
        (2, 'Reject')
    )
    accept_changes = models.IntegerField(choices=changes_decisions, default=2)

"""

# TODO: The ModificationPipelineRequest object needs to be created using the
# original Pipeline's primary key so the objects can be looked up together.
# Once the ModificationPipelineRequest object is approved, the default save needs
# to be overriden to delete the current ModificationPipelineRequest and update the
# original Pipeline.

Ignore above, just keeping to look back at thought process

History_change_reason_field should be changed to 'reason' so that the approval
or denial of a pipeline can be returned back to the user.
Also don't delete the modifcatio

Need a way to link mod requests to a pipeline
mod request need reason for accept / deny
views to look at reason pipeline changes happened or not

"""
