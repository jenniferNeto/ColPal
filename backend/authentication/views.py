from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import Http404

from .serializers import UsersSerializer, UserLoginSerializer

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

class UserLoginAPIView(generics.CreateAPIView):
    """
    Log a user in by their userid
    """
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        user = User.objects.filter(id=user_id).first()

        # 404 is user not found
        if user is None:
            raise Http404

        # Login user to system
        # This is using the PasswordlessAuthentication backend so the only
        # required attribute is the users' id number
        login(request, user)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
