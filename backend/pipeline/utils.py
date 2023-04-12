from .models import Pipeline, PipelineFile

from django.utils import timezone

from django.core.mail import send_mail

from datetime import datetime, timedelta

import math

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
    current_time: datetime = timezone.now()
    deadline: datetime = start_time + pipeline.upload_frequency

    # Calculate time remaining
    remaining_time: timedelta = deadline - current_time

    if remaining_time > timedelta(0):
        return remaining_time
    return timedelta(0)

def calculate_hard_deadline(pipeline_id: int) -> timedelta:
    """Claculate the hard deadline for a pipeline. This resets the deadline to upload_frequency on file upload"""
    try:
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        latest_upload = PipelineFile.objects.filter(pipeline=pipeline).last()
    except Pipeline.DoesNotExist:
        raise LookupError(f'Pipeline with id {pipeline_id} does not exist')

    if not pipeline.is_stable:
        # Time ran out
        return timedelta(0)

    # If pipeline is not approved files cannot be uploaded
    if not pipeline.approved_date:
        return pipeline.upload_frequency

    # Get the date of the last uploaded file to the current pipeline
    start_time: datetime = pipeline.approved_date
    current_time: datetime = timezone.now()

    elapsed_time: timedelta = current_time - start_time

    if elapsed_time <= timedelta(0):
        return pipeline.upload_frequency

    # Used to determine new cycle start time
    elapsed_period: float = elapsed_time / pipeline.upload_frequency

    # Calculate previous cycle start time to stop incrementing cycle when file was not uploaded previously
    previous_cycle_start_time: datetime = start_time + pipeline.upload_frequency * math.floor(elapsed_period - 1)
    deadline: datetime = start_time + pipeline.upload_frequency * math.ceil(elapsed_period)

    if latest_upload and latest_upload.upload_date < previous_cycle_start_time:
        # Pipeline is unstable
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

def cron_is_stable():
    for pipeline in Pipeline.objects.all():
        stable = is_stable(pipeline.pk)
        pipeline.is_stable = stable
        print("Pipeline Stability:", pipeline.is_stable)
        print("Remaining time:", calculate_remaining_time(pipeline.pk))
        print("Hard Deadline:", calculate_hard_deadline(pipeline.pk))
        print()

        # If pipeline was stable but now is unstable
        if pipeline.is_stable and not stable:
            # Send email to everyone on pipeline notifying of unstable pipeline
            pass

        # If pipeline was unstable but now is stable
        if not pipeline.is_stable and stable:
            # Send email to everyone on pipeline notifying of stable pipeline
            pass
