from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serialize base user accounts"""
    admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'admin',
        ]

    def get_admin(self, obj):
        return obj.is_superuser

class UserLoginSerializer(serializers.ModelSerializer):
    # Users can only login to created accounts using the api view
    user = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'user'
        ]

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'email'
        ]
