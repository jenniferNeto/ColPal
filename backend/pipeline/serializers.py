from rest_framework import serializers
from .models import Pipeline


class PipelineSerializer(serializers.ModelSerializer):
    # approved_date = serializers.SerializerMethodField()

    class Meta:
        model = Pipeline
        fields = [
            'title',
            'creation_date',
            'upload_frequency',
            'is_approved',
            'is_active',
            'approved_date'
        ]

    # def get_approved_date(self, obj):
    #     if obj is None:
    #         return None
    #     return obj.data
