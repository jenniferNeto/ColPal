from rest_framework import serializers

from .models import Viewer, Uploader, Manager

# I don't like how this code is repeated but when trying to abstract away
# the fields into a base class the serializer would complain that the fields
# attribute isn't set but setting it would mean the values need to be redeclared

class ViewerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source="viewer.pk")
    username = serializers.CharField(read_only=True, source='viewer.username')
    email = serializers.CharField(read_only=True, source='viewer.email')

    class Meta:
        model = Viewer

        fields = [
            'id',
            'username',
            'email'
        ]

class UploaderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source="uploader.pk")
    username = serializers.CharField(read_only=True, source='uploader.username')
    email = serializers.CharField(read_only=True, source='uploader.email')

    class Meta:
        model = Uploader

        fields = [
            'id',
            'username',
            'email'
        ]

class ManagerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, source="manager.pk")
    username = serializers.CharField(read_only=True, source='manager.username')
    email = serializers.CharField(read_only=True, source='manager.email')

    class Meta:
        model = Manager

        fields = [
            'id',
            'username',
            'email'
        ]
