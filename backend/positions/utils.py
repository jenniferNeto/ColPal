from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User, AbstractBaseUser
from django.utils import timezone
from django.conf import settings

from pipeline.models import Pipeline, PipelineNotification


def position_email(subject: str, pipeline_id: int, template: str, user, context):
    """Send a pipeline status template email"""
    pipeline = Pipeline.objects.get(pk=pipeline_id)

    message_html = render_to_string(template, context=context)
    message = strip_tags(message_html)
    try:
        email = EmailMultiAlternatives(
            subject,
            message,
            settings.SERVER_EMAIL,
            to=[user.email]  # type: ignore
        )
        email.attach_alternative(message_html, "text/html")
        email.send()
    except Exception:
        pass

    # Create pipeline notification
    PipelineNotification.objects.create(
        pipeline=pipeline,
        user=user,
        date=timezone.now(),
        message='Position Removed' if "removed" in subject else "Position Added")
