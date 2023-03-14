from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serialize base user accounts"""
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
        ]

class UserLoginSerializer(serializers.ModelSerializer):
    # Users can only login to created accounts using the api view
    user = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'user'
        ]
