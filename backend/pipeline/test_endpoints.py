from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

from request.models import Request
from positions.models import Uploader

from .models import Pipeline


class PipelineValidationEndpointTestCase(APITestCase):
    """Test cases for Pipeline that are based on validation"""

    def setUp(self):
        User.objects.all().delete()
        Pipeline.objects.all().delete()

        # Email and password don't matter in this context but are required to create a superuser
        User.objects.create_superuser(username="test", email="", password="")
        Pipeline.objects.create(title='Test Pipeline')

        # User needs to be logged in to access endpoints
        self.client.login(username="test")

    def test_pipelines_detailview_invalid(self):
        """Test the pipelines individal detail endpoint for failure"""
        response = self.client.get("/pipelines/2/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_updateview_get_invalid(self):
        """Test non-existant pipeline update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        response = self.client.get("/pipelines/2/update/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_updateview_put_invalid_upload_frequency(self):
        """Test the pipelines put update endpoint invalid upload frequency"""
        data = {'title': "Title", 'upload_frequency': "e", 'update_reason': "Updated", 'is_active': True}
        response = self.client.put("/pipelines/1/update/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pipelines_updateview_put_invalid_update_reason(self):
        """Test the pipelines put update endpoint invalid update_reason"""
        data = {'title': "Title", 'upload_frequency': "0", 'is_active': True}
        response = self.client.put("/pipelines/1/update/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pipelines_history_invalid(self):
        """Test the pipelines get history"""
        response = self.client.get("/pipelines/2/history/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_create(self):
        """Test the creation of a new pipeline"""
        data = {'title': "Title", 'upload_frequency': "0", 'is_active': False}
        response = self.client.post("/pipelines/create/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class PipelineEndpointTestCase(APITestCase):
    """Test cases for Pipeline endpoints"""
    authenticate = True
    status_code = status.HTTP_200_OK if authenticate else status.HTTP_403_FORBIDDEN

    def setUp(self):
        User.objects.all().delete()
        Pipeline.objects.all().delete()

        # Email and password don't matter in this context but are required to create a superuser
        User.objects.create_superuser(username="test", email="", password="")
        Pipeline.objects.create(title='Test Pipeline')

        # User needs to be logged in to access endpoints
        self.client.login(username="test")

    def test_pipelines_listview(self):
        """Test the pipelines listview endpoint"""
        response = self.client.get("/pipelines/", follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_detailview(self):
        """Test the pipelines individal detail endpoint"""
        response = self.client.get("/pipelines/1/", follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_updateview_get(self):
        """Test the pipelines get update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        response = self.client.get("/pipelines/1/update/", data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_updateview_manager_put(self):
        """Test the pipelines put update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        response = self.client.put("/pipelines/1/update/", data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 0)

    def test_pipelines_updateview_uploader_put(self):
        """Test the pipelines put update endpoint"""

        # A request is only created if the user is not a manager or superuser
        self.client.logout()
        Uploader.objects.create(user=User.objects.create_user("user"), pipeline=Pipeline.objects.all()[0])
        self.client.login(username="user")

        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        response = self.client.put("/pipelines/1/update/", data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 1)

        # Log out of the Uploader account and log into the superuser account again
        self.client.logout()
        self.client.login(username="test")

    def test_pipelines_history(self):
        """Test the pipelines get history"""
        response = self.client.get("/pipelines/1/history/", follow=True)
        self.assertEquals(response.status_code, self.status_code)

class AnonymousPipelineEndpointTestCase(PipelineEndpointTestCase):
    """Test cases for Anonymous Pipeline endpoints"""
    authenticate = False
    status_code = status.HTTP_200_OK if authenticate else status.HTTP_403_FORBIDDEN

    def setUp(self):
        Pipeline.objects.all().delete()
        Pipeline.objects.create(title='Test Pipeline')

    def test_pipelines_updateview_manager_put(self):
        """Test the pipelines put update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        response = self.client.put("/pipelines/1/update/", data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 0)

    def test_pipelines_updateview_uploader_put(self):
        """Test the pipelines put update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        response = self.client.put("/pipelines/1/update/", data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 0)
