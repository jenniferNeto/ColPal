from django.db import models
from django.contrib.auth import get_user_model

from pipeline.models import Pipeline

class PipelineUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True)
    pipeline_id = pipeline.primary_key

    class Meta:
        abstract = True

class Viewer(PipelineUser):
    class Meta:
        unique_together = ('user', 'pipeline')

class Uploader(PipelineUser):
    class Meta:
        unique_together = ('user', 'pipeline')

class Manager(PipelineUser):
    class Meta:
        unique_together = ('user', 'pipeline')
