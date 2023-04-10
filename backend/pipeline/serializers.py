from rest_framework import serializers

from .models import Pipeline, PipelineFile


class PipelineSerializer(serializers.ModelSerializer):
    """Serialize an entire user pipeline"""
    created = serializers.SerializerMethodField(read_only=True)
    last_modified = serializers.SerializerMethodField(read_only=True)

    approved = serializers.SerializerMethodField(read_only=True)
    approved_date = serializers.SerializerMethodField(read_only=True)

    upload_frequency = serializers.DurationField()

    class Meta:
        model = Pipeline

        fields = [
            'id',
            'title',
            'created',
            'last_modified',
            'upload_frequency',
            'is_active',
            'approved',
            'approved_date',
        ]

    # Get the following attributes as READ_ONLY from the Pipeline model
    # These attributes should only be modified by users with elevated permissions
    def get_created(self, obj):
        return obj.created

    def get_last_modified(self, obj):
        return obj.last_modified

    def get_approved_date(self, obj):
        return obj.approved_date

    def get_approved(self, obj):
        return obj.is_approved

    def get_upload_frequency(self, obj):
        return str(obj.upload_frequency.total_seconds())

class PipelineHistorySeralizer(PipelineSerializer):
    """
    Seralize the entire Pipeline object but include the
    history of pipeline modifications and a reason for
    modifying the object
    """
    history = serializers.SerializerMethodField()

    class Meta:
        model = Pipeline

        fields = [
            'id',
            'title',
            'created',
            'last_modified',
            'upload_frequency',
            'is_active',
            'approved',
            'approved_date',
            'history',
        ]

    def get_history(self, obj):
        hist = obj.history.all()
        return hist.values()

class PipelineUpdateSerializer(PipelineHistorySeralizer):
    """
    Serialize the entire Pipeline object but include the
    reason for updating a pipeline. This field will be used
    in place of the history.history_change_reason field
    """
    update_reason = serializers.CharField()

    class Meta:
        model = Pipeline

        fields = [
            'title',
            'upload_frequency',
            'update_reason',
            'is_active',
        ]

class PipelineStatusSerializer(serializers.ModelSerializer):
    """Serialize the approval status of a pipeline"""
    approved = serializers.BooleanField(source='is_approved')

    class Meta:
        model = Pipeline

        fields = [
            'approved',
        ]

    def is_approved(self, obj):
        return obj.is_approved

class FileUploadSerializer(serializers.Serializer):
    """Serialize an uploaded file for a pipeline"""
    file = serializers.FileField()

    class Meta:
        model = PipelineFile

        fields = [
            'file'
        ]

class PipelineFileSerializer(serializers.Serializer):
    pipeline_id = serializers.SerializerMethodField()
    file_id = serializers.SerializerMethodField()
    path = serializers.SerializerMethodField()
    upload_date = serializers.SerializerMethodField()

    class Meta:
        model = PipelineFile

        fields = [
            'pipeline_id',
            'file_id',
            'file',
            'path',
            'upload_date'
        ]

    def get_pipeline_id(self, obj):
        return obj.pipeline.pk

    def get_file_id(self, obj):
        return obj.pk

    def get_path(self, obj):
        return obj.path

    def get_upload_date(self, obj):
        return obj.upload_date
