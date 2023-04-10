from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

import json


class UsersEndpointTestCase(APITestCase):
    """
    Test cases for Users endpoints
    """
    def setUp(self):
        # Email and password don't matter in this context but are required to create a superuser
        User.objects.create_superuser(username="test", email="", password="")

    def login(self):
        # User needs to be logged in to access endpoints
        self.client.login(username="test")
        data = {'username': "test", 'password': "."}
        response = self.client.post("/users/obtain/", data=data, follow=True)
        return json.loads(response.content)['access']

    def test_user_login(self):
        """Test the user's ability to login"""
        data = {'user': "1"}
        response = self.client.post("/users/login/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid(self):
        """Test the user's ability to login"""
        data = {'user': "-1"}
        response = self.client.post("/users/login/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_logout(self):
        """Test the user's ability to logout"""
        token = self.login()
        response = self.client.post("/users/logout/", HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_logout_invalid(self):
        """Test the user's ability to logout invalid request with user not logged in"""
        response = self.client.post("/users/logout/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
