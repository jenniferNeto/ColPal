from django.utils.dateparse import parse_duration

from .models import Request


def createRequest(data, instance):
    # Create a new pipeline modification request
    mod = Request.objects.create(title="Blank", pipeline=instance)

    mod.title = data['title']
    mod.upload_frequency = parse_duration(data['upload_frequency'])  # type: ignore
    mod.is_stable = 'is_stable' in data
    mod.hard_deadline = 'hard_deadline' in data
    mod.update_reason = data['update_reason']
    mod.save()
