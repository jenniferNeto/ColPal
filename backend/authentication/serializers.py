from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]

class UserLoginSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'user_id'
        ]
