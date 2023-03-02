from rest_framework import serializers
from simple_history.models import HistoricalRecords
from django.db.models import Exists

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
    # update_reason = serializers.CharField(required=False)

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
            'approved_date',
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

class PipelineHistorySeralizer(PipelineSerializer):
    """
    Seralize the entire Pipeline object but include the
    history of pipeline modifications and a reason for
    modifying the object
    """
    history = serializers.SerializerMethodField()
    updated_reason = serializers.SerializerMethodField()

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
            'updated_reason',
            'history',
        ]

    # def get_update_reason(self, obj):
    #     return obj.update_reason

    def get_history(self, obj):
        print(obj.__dict__)
        # hist = obj.history.all().annotate(update_reason="")
        hist = obj.history.all()
        # print("History values: ", hist.values())
        return hist.values()

    def get_updated_reason(self, obj):
        hist = obj.history.all().values()
        print("PLEASE WHEN IS THIS GETTING CALLED", hist)
        return obj.history.all().values_list('history_change_reason')
