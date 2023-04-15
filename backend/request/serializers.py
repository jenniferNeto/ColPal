from rest_framework import serializers

from .models import Request
from pipeline.serializers import PipelineSerializer


class RequestSerializer(serializers.ModelSerializer):
    request_id = serializers.SerializerMethodField()
    request_status = serializers.SerializerMethodField()
    pipeline_id = serializers.SerializerMethodField()
    update_reason = serializers.SerializerMethodField()

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

    def get_update_reason(self, obj):
        return obj.update_reason

    def to_representation(self, instance):
        # data = PipelineSerializer().to_representation(instance)
        # output = dict()
        # # handle custom serialization for each field here
        # for field_name, field_value in data.items():
        #     old, old_val = f'old_{field_name}', getattr(instance, field_name)
        #     new, new_val = f'new_{field_name}', field_value

        #     if old_val != new_val:
        #         output[old] = old_val
        #         output[new] = new_val
        # return output

        # I'm not sure how to check this automatically for each attribute
        # Just going to manually check for now until a better solution is found
        representation = super().to_representation(instance)
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

        new_hard_deadline = instance.hard_deadline
        old_hard_deadline = instance.pipeline.hard_deadline

        if new_hard_deadline != old_hard_deadline:
            representation['request_hard_deadline'] = new_hard_deadline
            representation['hard_deadline'] = old_hard_deadline

        return representation

class RequestUpdateSerializer(RequestSerializer):
    """Serialize the update requests"""
    changes_decisions = ['Pending', 'Approved', 'Rejected']
    update_reason = serializers.CharField()

    class Meta(RequestSerializer.Meta):
        fields = [
            'accept_changes',
            'response',
        ]

    def get_accept_changes(self, obj):
        status = obj.accept_changes
        changes_decisions = ['Pending', 'Accepted', 'Rejected']
        return changes_decisions[status]
