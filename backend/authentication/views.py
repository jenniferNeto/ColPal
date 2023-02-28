from rest_framework import generics
from django.contrib.auth.models import User

from .serializers import UsersSerializer

class UsersListAPIView(generics.ListAPIView):
    """
    Expose all users to the API
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer


class UsersDetailAPIView(generics.RetrieveAPIView):
    """
    Expose a user to the API using the user id number
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
