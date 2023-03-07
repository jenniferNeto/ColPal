from rest_framework import serializers

from .models import Request

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

class RequestUpdateSerializer(RequestSerializer):
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
    
"""

The Request Update API needs to show a dropdown menu that allows the manager
to choose weather to accept or reject the current changes.

If these changes are accepted, the request object should override the details
in the pipeline object that it has attached to it. This update will also make
the simple_history plugin update the history of the object.

Right now the problem is that the UpdateAPIView is not including the extra field
to actually update the model itself. 

Also the RequestUpdateSerializer model probably shouldn't use __all__ as the fields
option. This is including duplicate fields such as "id": 9 and "request_id": 9.

After all of the previous steps are done and Pipelines can finally be updated using
the API, create test cases for all the API endpoints. This doesn't have to be done
anytime soon.

After all of that is done: Go through the code and remove any unused imports.
Comment the code more and get some better documentation so it's easier to read
for everyone else.

"""
