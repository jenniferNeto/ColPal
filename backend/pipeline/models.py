from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

class Pipeline(models.Model):
    title = models.CharField(max_length=40)
    # created_by = models.ForeignKey(get_user_model)
    creation_date = models.DateTimeField(default=datetime.now)
    upload_frequency = models.DurationField(default=timedelta)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    approved_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        pass
        # permissions = [
        #     ("view_pipeline", "Can view pipelines"),
        # ]
