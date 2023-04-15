from rest_framework import serializers

from .models import Pipeline, PipelineFile, PipelineNotification


class ConstraintSerializer(serializers.Serializer):
    column_name = serializers.CharField()
    column_type = serializers.CharField()

class ConstraintListSerializer(serializers.Serializer):
    constraints = ConstraintSerializer(many=True)

class PipelineSerializer(serializers.ModelSerializer):
    """Serialize an entire user pipeline"""
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # handle custom serialization for each field here
        for field_name, field_value in data.items():
            data[field_name] = field_value
        return data

    class Meta:
        model = Pipeline

        fields = '__all__'

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
            'is_stable',
            'hard_deadline',
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
            'hard_deadline',
            'update_reason',
        ]

class PipelineStatusSerializer(serializers.ModelSerializer):
    """Serialize the approval status of a pipeline"""
    approved = serializers.BooleanField(source='is_approved')

    class Meta:
        model = Pipeline

        fields = [
            'approved',
        ]

class FileUploadSerializer(serializers.ModelSerializer):
    """Serialize an uploaded file for a pipeline"""
    file = serializers.FileField()

    class Meta:
        model = Pipeline

        fields = [
            'file',
        ]

    def get_file(self, obj):
        return obj.file

class PipelineFileSerializer(serializers.Serializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # handle custom serialization for each field here
        for field_name, field_value in data.items():
            data[field_name] = field_value
        return data

    class Meta:
        model = PipelineFile

        fields = '__all__'

class PipelineNotificationSerializer(serializers.ModelSerializer):
    """Serialize the approval status of a pipeline"""
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # handle custom serialization for each field here
        for field_name, field_value in data.items():
            data[field_name] = field_value
        return data

    class Meta:
        model = PipelineNotification

        fields = '__all__'
