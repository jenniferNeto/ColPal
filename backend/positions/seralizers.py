from rest_framework import serializers
from .models import Viewer, Uploader, Manager

class ViewerSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Viewer

        fields = [
            'viewer',
            'pipeline'
        ]

class UploaderSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Uploader

        fields = [
            'uploader',
            'pipeline',
        ]

class ManagerSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Manager

        fields = [
            'manager',
            'pipeline',
        ]
