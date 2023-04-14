from .models import Pipeline, PipelineFile

from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth.models import User

from datetime import datetime, timedelta

from email.mime.text import MIMEText

from django.template.loader import render_to_string, get_template

from positions.models import Viewer, Uploader, Manager

import math

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
    for pipeline in Pipeline.objects.all():
        stable = is_stable(pipeline.pk)

        print("Pipeline Stability:", pipeline.is_stable)
        print("Remaining time:", calculate_remaining_time(pipeline.pk))
        print("Hard Deadline:", calculate_hard_deadline(pipeline.pk))
        print()

        # If pipeline was stable but now is unstable
        if pipeline.is_stable and not stable:
            # Send email to everyone on pipeline notifying of unstable pipeline
            users = extract_users(pipeline.pk)
            stable_email("[Stable Data] Your pipeline is unstable!",
                         pipeline.pk, os.environ.get("EMAIL_ADDRESS", ''), users)

            print("Template:", render_to_string("base.html"))

        # If pipeline was unstable but now is stable
        if not pipeline.is_stable and stable:
            # Send email to everyone on pipeline notifying of stable pipeline
            users = extract_users(pipeline.pk)
            stable_email("[Stable Data] Your pipeline is stable again!",
                         pipeline.pk, os.environ.get("EMAIL_ADDRESS", ''), users)

        if pipeline.is_stable != stable:
            pipeline.is_stable = stable
            pipeline.save()

def stable_email(subject: str, pipeline_id: int, from_email: str, recipient_list):
    print("Starting email process")
    pipeline = Pipeline.objects.get(pk=pipeline_id)

    # Extract all users with a non-blank email address
    users = [user for user in recipient_list if user.email != '']

    stable = "Stable" if not pipeline.is_stable else "Unstable"

    for recipient in users:
        message_html = render_to_string('base.html', context={})
        message = MIMEText(message_html, 'html')
        print("Sending mail:", send_mail(
            subject=subject,
            message=message.as_string(),
            from_email=from_email,
            recipient_list=[recipient.email]))


# message = f'Pipeline Notice\n \
#         Pipline ID: #{pipeline.pk}\n \
#         Pipeline Title: {pipeline}\n \
#         Status: {stable}\n \
#         Update Time: {datetime.now().strftime("%H:%M:%S %m/%d/%Y")}\n \
#         \n \
#         To view more information on this pipeline please login at https://stabledata.net/login'