from .models import Pipeline, PipelineFile

from django.utils import timezone

def is_stable(pipeline_id: int) -> bool:
    try:
        pipeline = Pipeline.objects.get(pk=pipeline_id)
        latest_upload = PipelineFile.objects.filter(pipeline=pipeline).last()
    except Pipeline.DoesNotExist:
        raise LookupError(f'Pipeline with id {pipeline_id} does not exist')

    # Get the date of the last uploaded file to the current pipeline
    start_date = pipeline.created if latest_upload is None else latest_upload.upload_date

    # Calculate if the pipeline is stale
    return start_date + pipeline.upload_frequency < timezone.now()
