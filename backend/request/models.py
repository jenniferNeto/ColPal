from django.db import models

from pipeline.models import Pipe, Pipeline

class Request(Pipe):
    update_reason = models.TextField(null=True)
    pipeline = models.ForeignKey(Pipeline, null=True, on_delete=models.CASCADE)
    pipeline_id = pipeline.primary_key

    changes_decisions = (
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'Rejected')
    )
    accept_changes = models.IntegerField(choices=changes_decisions, default=0)
