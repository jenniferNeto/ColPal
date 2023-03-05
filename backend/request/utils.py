from django.utils.dateparse import parse_duration

from .models import Request


def createRequest(data, instance):
    mod = Request.objects.create(title="Blank", pipeline=instance)

    mod.title = data['title']
    mod.upload_frequency = parse_duration(data['upload_frequency'])
    mod.is_active = True if 'is_acitve' in data else False
    mod.update_reason = data['update_reason']
    mod.save()
