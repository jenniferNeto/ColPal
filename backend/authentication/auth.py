from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.backends import ModelBackend


class PasswordlessAuthentication(ModelBackend):
    """
    Authenticate regular users without checking their password
    Admin users are still authenticated using the username and password combination
    ** This module should be replaced with a real custom backend authentication module **
    """
    def authenticate(self, request, username=None, password=""):
        try:
            """
            Disabled admin password checking for frontend demo purposes only
            DO NOT KEEP THIS AS THE BACKEND AUTH SYSTEM IN A REAL PROJECT WITH 
            SENSITIVE DATA! THERE IS NO REAL AUTHENTICATION FOR ANY OF THESE REQUESTS
            """
            user = User.objects.get(username=username)
            # if user.is_superuser and user.check_password(password):
            #     return user
            # # Regular users 'need' a password but it won't be used to authenticate
            # elif not user.is_superuser:
            #     return user
            # else:
            #     return None
            return user
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
