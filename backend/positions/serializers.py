from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from pipeline.models import Pipeline

from .models import Viewer, Uploader, Manager

class PipelineUserSerializer(serializers.ModelSerializer):
    """
    Base position serializer that serializers the user foreign key
    Subclasses of this class need to set a model in the Meta innerclass
    """
    id = serializers.IntegerField(read_only=True, source="user.pk")
    username = serializers.CharField(read_only=True, source='user.username')
    email = serializers.CharField(read_only=True, source='user.email')

    class Meta:
        fields = [
            'id',
            'username',
            'email'
        ]

class ViewerSerializer(PipelineUserSerializer):
    class Meta(PipelineUserSerializer.Meta):
        model = Viewer

class UploaderSerializer(PipelineUserSerializer):
    class Meta(PipelineUserSerializer.Meta):
        model = Uploader

class ManagerSerializer(PipelineUserSerializer):
    class Meta(PipelineUserSerializer.Meta):
        model = Manager

class PositionCreateSerializer(serializers.ModelSerializer):
    # Show the userid instead of the user itself for post purposes
    # TODO: This line of code is causing the makemigrations to fail. It's 4:30AM so I'm going to bed now
    # TODO: Figure out why this line is making everything fail. Stack trace is annoying to read but it should help
    user = serializers.ChoiceField(choices=User.objects.all().values().values_list('pk', flat=True))

    class Meta:
        fields = ['user']

    def get_pipeline(self, obj):
        return obj.pipeline

class ViewerCreateSerializer(PositionCreateSerializer):
    class Meta(PositionCreateSerializer.Meta):
        model = Viewer

class UploaderCreateSerializer(PositionCreateSerializer):
    class Meta(PositionCreateSerializer.Meta):
        model = Uploader

class ManagerCreateSerializer(PositionCreateSerializer):
    class Meta(PositionCreateSerializer.Meta):
        model = Manager
