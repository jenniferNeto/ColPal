from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.http import Http404

from .serializers import UserSerializer, UserLoginSerializer


class UsersListAPIView(generics.ListAPIView):
    """Expose all users to the API"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UsersDetailAPIView(generics.RetrieveAPIView):
    """Expose a user to the API using the user id number"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginAPIView(generics.CreateAPIView):
    """Log a user in by their userid"""
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Get a user based on the login info of the user
        user_id = request.data['user']
        user = User.objects.filter(id=user_id).first()

        # 404 is user not found
        if user is None:
            raise Http404

        # Login user into system
        # This is using the PasswordlessAuthentication backend so the only
        # required attribute is the users' id number
        login(request, user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogoutAPIView(APIView):
    """Log a user out"""
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Don't need any validation or serialization here
        # Honor every logout request made
        logout(request)

        return Response(status=status.HTTP_200_OK)
