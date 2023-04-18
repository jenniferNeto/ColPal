from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Viewer, Uploader, Manager

User = get_user_model()


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

class PositionSerializer(serializers.ModelSerializer):
    # Show the userid instead of the user itself for post purposes
    id = serializers.IntegerField()

    class Meta:
        fields = [
            'id',
        ]

class ViewerPositionSerializer(PositionSerializer):
    class Meta(PositionSerializer.Meta):
        model = Viewer

class UploaderPositionSerializer(PositionSerializer):
    class Meta(PositionSerializer.Meta):
        model = Uploader

class ManagerPositionSerializer(PositionSerializer):
    class Meta(PositionSerializer.Meta):
        model = Manager
