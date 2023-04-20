from .models import Pipeline, PipelineFile

from django.utils import timezone
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from datetime import datetime, timedelta

from positions.models import Viewer, Uploader, Manager
from pipeline.models import PipelineNotification

import snowflake.connector

import os

def calculate_remaining_time(pipeline_id: int) -> timedelta:
    """Calculate the remaining time left for a pipeline to be stable"""
    try:
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        latest_upload = PipelineFile.objects.filter(pipeline=pipeline).last()
    except Pipeline.DoesNotExist:
        raise LookupError(f'Pipeline with id {pipeline_id} does not exist')

    # If pipeline is not approved files cannot be uploaded
    if not pipeline.approved_date:
        return pipeline.upload_frequency

    # Get the date of the last uploaded file to the current pipeline
    start_time: datetime = pipeline.approved_date if latest_upload is None else latest_upload.upload_date

    # End of the current upload cycle
    deadline: datetime = start_time + pipeline.upload_frequency

    # Calculate time remaining
    remaining_time: timedelta = deadline - timezone.now()

    # Time remaining shouldn't be negative
    if remaining_time > timedelta(0):
        return remaining_time
    return timedelta(0)

def calculate_hard_deadline(pipeline_id: int) -> timedelta:
    """Calculate the hard deadline for a pipeline. This resets the deadline to upload_frequency on file upload"""
    try:
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        latest_upload = PipelineFile.objects.filter(pipeline=pipeline).last()
    except Pipeline.DoesNotExist:
        raise LookupError(f'Pipeline with id {pipeline_id} does not exist')

    # If pipeline is not approved files cannot be uploaded
    if not pipeline.approved_date:
        return pipeline.upload_frequency

    # Get the date of the last uploaded file to the current pipeline
    start_time: datetime = pipeline.approved_date
    current_time: datetime = timezone.now()

    elapsed_time: timedelta = current_time - start_time
    try:
        # Used to determine new cycle start time
        elapsed_period = elapsed_time // pipeline.upload_frequency
    except ZeroDivisionError:
        return timedelta(0)

    # Calculate cycle start times
    cycle_start: datetime = start_time + pipeline.upload_frequency * elapsed_period
    deadline: datetime = cycle_start + pipeline.upload_frequency
    previous_cycle: datetime = cycle_start - pipeline.upload_frequency

    # At least one cycle has completed
    if elapsed_period >= 1:
        # File hasn't been uploaded
        if not latest_upload:
            return timedelta(0)

        # If a file wasn't uploaded in the last cycle the deadline has been reached
        if latest_upload.upload_date < previous_cycle:
            return timedelta(0)

    return deadline - current_time

def get_deadline(pipeline_id: int) -> timedelta:
    """Get remaining time based on type of deadline"""
    try:
        pipeline = Pipeline.objects.get(pk=pipeline_id)
    except Pipeline.DoesNotExist:
        raise LookupError(f'Pipeline with id {pipeline_id} does not exist')

    if pipeline.hard_deadline:
        return calculate_hard_deadline(pipeline_id)
    return calculate_remaining_time(pipeline_id)

def is_stable(pipeline_id: int) -> bool:
    """Verify a pipeline is stable by checking remaining time"""
    return get_deadline(pipeline_id) != timedelta(0)

def extract_users(pipeline_id: int):
    try:
        pipeline = Pipeline.objects.get(pk=pipeline_id)
    except Pipeline.DoesNotExist:
        raise LookupError(f'Pipeline with id {pipeline_id} does not exist')

    # Get all users on a pipeline
    viewers = Viewer.objects.filter(pipeline=pipeline)
    uploaders = Uploader.objects.filter(pipeline=pipeline)
    managers = Manager.objects.filter(pipeline=pipeline)

    users = [obj.user for obj in viewers]
    users.extend([obj.user for obj in uploaders])
    users.extend([obj.user for obj in managers])

    # Remove duplicates
    users_filter = []
    [users_filter.append(user) for user in users if user not in users_filter]

    return users_filter

def cron_is_stable():
    """Validate stability conditions of all pipelines and notify users of changes"""
    for pipeline in Pipeline.objects.all():
        stable = is_stable(pipeline.pk)

        # If pipeline was stable but now is unstable
        if pipeline.is_stable and not stable:
            # Send email to everyone on pipeline notifying of unstable pipeline
            users = extract_users(pipeline.pk)
            stable_email("Your pipeline is unstable!",
                         pipeline.pk, 'unstable.html', os.environ.get("EMAIL_ADDRESS", ''), users)

        # If pipeline was unstable but now is stable
        if not pipeline.is_stable and stable:
            # Send email to everyone on pipeline notifying of stable pipeline
            users = extract_users(pipeline.pk)
            stable_email("Your pipeline is stable again!",
                         pipeline.pk, 'stable.html', os.environ.get("EMAIL_ADDRESS", ''), users)

        # If the stability of the pipeline changed, update the object
        if pipeline.is_stable != stable:
            pipeline.is_stable = stable
            pipeline.save()

def stable_email(subject: str, pipeline_id: int, template: str, from_email: str, recipient_list):
    """Send a pipeline status template email"""
    pipeline = Pipeline.objects.get(pk=pipeline_id)

    # Extract all users with a non-blank email address
    users = [user for user in recipient_list if user.email != '']

    # Send every user a status update email
    for recipient in users:
        message_html = render_to_string(template, context={'username': recipient, 'title': pipeline})
        message = strip_tags(message_html)
        try:
            email = EmailMultiAlternatives(
                subject,
                message,
                from_email,
                to=[recipient.email]
            )
            email.attach_alternative(message_html, "text/html")
            email.send()
        except Exception:
            pass

        # Create pipeline notification
        PipelineNotification.objects.create(
            pipeline=pipeline,
            user=recipient,
            date=timezone.now(),
            message='Stable' if pipeline.is_stable else 'Unstable')

def get_snowflake_files():
    connection = snowflake.connector.connect(
        user='SMA237',
        account='BBOSMPR.FY01681',
        authenticator='externalbrowser',
        warehouse='COLPAL_DSP_WAREHOUSE',
        database='COLPAL_DSP_DATABASE',
        token=os.environ.get('SNOWFLAKE_BEARER')
    )

    cursor = connection.connect()
    query = "LIST @gcs_stage"

    cursor.execute(query)  # type: ignore

    results = cursor.fetchall()  # type: ignore
    return results
