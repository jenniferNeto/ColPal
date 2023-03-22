<<<<<<< HEAD
from django.utils.dateparse import parse_duration

from .models import Request


def createRequest(data, instance):
    # Create a new pipeline modification request
    mod = Request.objects.create(title="Blank", pipeline=instance)

    mod.title = data['title']
    mod.upload_frequency = parse_duration(data['upload_frequency'])
    mod.is_active = True if 'is_acitve' in data else False
    mod.update_reason = data['update_reason']
    mod.save()
=======
from django.utils.dateparse import parse_duration

from .models import Request


def createRequest(data, instance):
    # Create a new pipeline modification request
    mod = Request.objects.create(title="Blank", pipeline=instance)

    mod.title = data['title']
    mod.upload_frequency = parse_duration(data['upload_frequency'])  # type: ignore
    mod.is_active = 'is_active' in data
    mod.update_reason = data['update_reason']
    mod.save()
>>>>>>> 67abf97cb6b43bec49e23020ffb2efb7720b06a1
