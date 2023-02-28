from django.db import models
from datetime import datetime, timedelta

class Pipeline(models.Model):
    title = models.CharField(max_length=40)
    creation_date = models.DateTimeField(default=datetime.now)
    upload_frequency = models.DurationField(default=timedelta)

    class Meta:
        pass
        # permissions = [
        #     ("view_pipeline", "Can view pipelines"),
        # ]
