from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend


class PasswordlessAuthentication(ModelBackend):
    """
    Authenticate users without checking their password. This module should be deleted during production and the
    backend/settings.py should have the AUTHENTICATION_BACKENDS flag deleted. ***CURRENTLY DISABLED TO LOG INTO THE ADMIN***
    """
    def authenticate(self, request, username=None):
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
