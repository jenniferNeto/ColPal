from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from pipeline.models import Pipeline

class PipelineUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True)
    pipeline_id = pipeline.primary_key

    class Meta:
        unique_together = ('user', 'pipeline')

class Viewer(models.Model):
    viewer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True)
    pipeline_id = pipeline.primary_key

    class Meta:
        unique_together = ('viewer', 'pipeline')

class Uploader(models.Model):
    uploader = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True)
    pipeline_id = pipeline.primary_key

    class Meta:
        unique_together = ('uploader', 'pipeline')

class Manager(models.Model):
    manager = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True)
    pipeline_id = pipeline.primary_key

    class Meta:
        unique_together = ('manager', 'pipeline')
