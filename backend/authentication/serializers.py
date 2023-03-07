from rest_framework import serializers
from django.contrib.auth.models import User

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
    user = serializers.ChoiceField(choices=User.objects.all().values().values_list('pk', flat=True))

    class Meta:
        model = User
        fields = [
            'user'
        ]
