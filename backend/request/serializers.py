from rest_framework import serializers

from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    request_id = serializers.SerializerMethodField()
    request_status = serializers.SerializerMethodField()
    pipeline_id = serializers.SerializerMethodField()

    class Meta:
        model = Request

        fields = [
            'request_id',
            'request_status',
            'update_reason',
            'pipeline_id'
        ]

    def get_request_id(self, obj):
        return obj.pk

    def get_request_status(self, obj):
        status = obj.accept_changes
        changes_decisions = ['Pending', 'Accepted', 'Rejected']
        return changes_decisions[status]

    def get_pipeline_id(self, obj):
        return obj.pipeline.pk

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # I'm not sure how to check this automatically for each attribute
        # Just going to manually check for now until a better solution is found
        new_title = instance.title
        old_title = instance.pipeline.title

        if new_title != old_title:
            representation['request_title'] = new_title
            representation['title'] = old_title

        new_upload_frequency = instance.upload_frequency
        old_upload_frequency = instance.pipeline.upload_frequency

        if new_upload_frequency != old_upload_frequency:
            representation['request_upload_frequency'] = new_upload_frequency
            representation['upload_frequency'] = old_upload_frequency

        new_is_active = instance.is_active
        old_is_active = instance.pipeline.is_active

        if new_is_active != old_is_active:
            representation['request_is_active'] = new_is_active
            representation['is_active'] = old_is_active

        return representation
