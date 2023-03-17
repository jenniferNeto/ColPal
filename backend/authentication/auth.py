from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.backends import ModelBackend


class PasswordlessAuthentication(ModelBackend):
    """Don't requre a password for users to login"""

    def authenticate(self, request, username=None, password=""):
        # Get a user object if it exists
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
