from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

import json


class UsersEndpointTestCase(APITestCase):
    """Test cases for Users endpoints"""
    def setUp(self):
        # Email and password don't matter in this context but are required to create a superuser
        User.objects.create_superuser(username="test", email="", password="")

    def login(self):
        # User needs to be logged in to access endpoints
        self.client.login(username="test")
        data = {'username': "test", 'password': "."}
        response = self.client.post("/users/obtain/", data=data, follow=True)
        return json.loads(response.content)['access']

    def test_user_list(self):
        """Testing endpoint to view all user accounts"""
        response = self.client.get("/users/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_detail(self):
        """Testing endpoint to view user details"""
        self.login()
        user_id = User.objects.get(username="test").pk
        response = self.client.get(f"/users/{user_id}/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_detail_invalid(self):
        """Testing endpoint to view user details"""
        self.login()
        response = self.client.get("/users/-1/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_login(self):
        """Test the user's ability to login"""
        user_id = User.objects.get(username="test").pk
        data = {'user': user_id}
        response = self.client.post("/users/login/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid(self):
        """Test the user's ability to login"""
        data = {'user': "-1"}
        response = self.client.post("/users/login/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_logout(self):
        """Test the user's ability to logout"""
        self.login()
        response = self.client.post("/users/logout/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_user_logout_invalid(self):
        """Test the user's ability to logout invalid request with user not logged in"""
        response = self.client.post("/users/logout/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user(self):
        """Test the user's ability to create a new user"""
        self.login()
        data = {'username': '.', 'email': '.'}
        response = self.client.post("/users/create/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid(self):
        """Test the user's ability to create a new user"""
        self.login()
        data = {'username': 'test', 'email': '.'}
        response = self.client.post("/users/create/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        """Test the user's ability to delete a user"""
        new_user = User.objects.create_user(username='test_dummy')
        self.login()
        data = {'user': new_user.pk}
        response = self.client.post("/users/delete/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_user_self(self):
        """Test the user's ability to delete a user"""
        self.login()
        user_id = User.objects.get(username="test").pk
        data = {'user': user_id}
        response = self.client.post("/users/delete/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user_invalid(self):
        """Test the user's ability to delete a user"""
        self.login()
        data = {'user': -1}
        response = self.client.post("/users/delete/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
