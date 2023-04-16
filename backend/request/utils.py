from django.utils.dateparse import parse_duration

from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from pipeline.models import PipelineNotification
from positions.models import Manager
from .models import Request


def create_pipeline_request(request, data, instance):
    # Create a new pipeline modification request
    mod = Request.objects.create(title="", pipeline=instance, user=request.user)

    mod.title = data['title']
    mod.upload_frequency = parse_duration(data['upload_frequency'])  # type: ignore
    mod.is_stable = 'is_stable' in data
    mod.hard_deadline = 'hard_deadline' in data
    mod.update_reason = data['update_reason']
    mod.save()

    # Send email
    send_request_email(mod)

def send_request_email(request: Request):
    """Send email to all managers on a pipeline about new request"""
    managers = Manager.objects.filter(pipeline=request.pipeline)
    for manager in managers:
        if manager.user:
            message_html = render_to_string(
                "request.html",
                context={'username': manager.user.get_username(), 'title': manager.pipeline})
            message = strip_tags(message_html)
            try:
                email = EmailMultiAlternatives(
                    "Your pipeline has a new request",
                    message,
                    from_email=settings.SERVER_EMAIL,
                    to=[manager.user.email]  # type: ignore
                )
                email.attach_alternative(message_html, "text/html")
                email.send()
                PipelineNotification.objects.create(
                    pipeline=request.pipeline,
                    user=request.user,
                    date=request.created,
                    message='New request')
            except Exception:
                pass

def send_request_status_email(request: Request):
    """Send email to all managers on a pipeline about new request"""
    message_html = render_to_string(
        "accepted.html" if request.accept_changes == 1 else "rejected.html",
        context={"username": request.user, "request_id": request.pk, "note": request.response})
    message = strip_tags(message_html)
    text = "Your pipeline request has been "
    try:
        email = EmailMultiAlternatives(
            text + "accepted" if request.accept_changes == 1 else text + "rejected",
            message,
            from_email=settings.SERVER_EMAIL,
            to=[request.user.email]  # type: ignore
        )
        email.attach_alternative(message_html, "text/html")
        email.send()
        PipelineNotification.objects.create(
            pipeline=request.pipeline,
            user=request.user,
            date=request.created,
            message="Accepted" if request.accept_changes == 1 else "Rejected")
    except Exception:
        pass
