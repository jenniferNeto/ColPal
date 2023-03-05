from rest_framework import serializers

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
