from rest_framework import serializers
from .models import Pipeline


class PipelineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pipeline
        fields = [
            'title',
            'creation_date',
            'upload_frequency'
        ]
