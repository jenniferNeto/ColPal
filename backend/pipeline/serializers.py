from rest_framework import serializers
from .models import Pipeline


class PipelineSerializer(serializers.ModelSerializer):
    # Creator needs to be null for now because people who aren't logged in
    # can view the pipelines. Need to set up authentication before allowing
    # people to view pipelines

    # creator = serializers.SerializerMethodField('_user')
    created = serializers.SerializerMethodField(read_only=True)
    last_modified = serializers.SerializerMethodField(read_only=True)

    approved = serializers.SerializerMethodField(read_only=True)
    approved_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pipeline

        fields = [
            'id',
            'title',
            # 'creator',
            'created',
            'last_modified',
            'upload_frequency',
            'is_active',
            'approved',
            'approved_date'
        ]

    # def get_creator(self, obj):
    #     request = self.context.get('request', None)
    #     if request:
    #         return request.user

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
