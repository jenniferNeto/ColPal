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
    user = serializers.ChoiceField(choices=User.objects.all().values().values_list('pk', flat=True))

    class Meta:
        model = User
        fields = [
            'user'
        ]
