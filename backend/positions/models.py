from django.db import models
from django.contrib.auth import get_user_model

from pipeline.models import Pipeline


class PipelineUser(models.Model):
    """All Positions are PipelineUsers"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, null=True)
    pipeline_id = pipeline.primary_key

    class Meta:
        abstract = True

class Viewer(PipelineUser):
    # Can only view, get
    class Meta:
        unique_together = ('user', 'pipeline')

class Uploader(PipelineUser):
    # Can view and request pipeline updates
    class Meta:
        unique_together = ('user', 'pipeline')

class Manager(PipelineUser):
    # Can view, modfiy, and approve pipeline requests
    class Meta:
        unique_together = ('user', 'pipeline')
