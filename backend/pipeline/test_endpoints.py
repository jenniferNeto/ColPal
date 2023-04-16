from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

import json

from request.models import Request
from positions.models import Viewer, Uploader, Manager

from .models import Pipeline


class PipelineValidationEndpointTestCase(APITestCase):
    """Test cases for Pipeline that are based on validation"""

    def setUp(self):
        # Email and password don't matter in this context but are required to create a superuser
        User.objects.create_superuser(username="test", email="", password="")
        Pipeline.objects.create(title='Test Pipeline')

    def login(self):
        # Login as a superuser for each test, individual tests may override
        self.client.login(username="test")

        # Get auth token
        data = {'username': "test", 'password': "."}
        response = self.client.post("/users/obtain/", data=data, follow=True)
        return json.loads(response.content)['access']

    def test_pipelines_detailview_invalid(self):
        """Test the pipelines individal detail endpoint for failure"""
        token = self.login()
        response = self.client.get("/pipelines/0/", HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_updateview_get_invalid(self):
        """Test non-existant pipeline update endpoint"""
        token = self.login()
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_stable': True}
        response = self.client.get("/pipelines/0/update/",
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token), data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_updateview_put_invalid_upload_frequency(self):
        """Test the pipelines put update endpoint invalid upload frequency"""
        token = self.login()
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        data = {'title': "Title", 'upload_frequency': "e", 'update_reason': "Updated", 'is_stable': True}
        response = self.client.put(f'/pipelines/{pipeline_id}/update/',
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token), data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pipelines_updateview_put_invalid_update_reason(self):
        """Test the pipelines put update endpoint invalid update_reason"""
        token = self.login()
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        data = {'title': "Title", 'upload_frequency': "0", 'is_stable': True}
        response = self.client.put(f'/pipelines/{pipeline_id}/update/',
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token), data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pipelines_history_invalid(self):
        """Test the pipelines get history"""
        token = self.login()
        response = self.client.get("/pipelines/0/history/", HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_create(self):
        """Test the creation of a new pipeline"""
        token = self.login()
        data = {'title': "Title", 'upload_frequency': "0", 'is_stable': False}
        response = self.client.post("/pipelines/create/",
                                    HTTP_AUTHORIZATION='Bearer {}'.format(token), data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

class PipelineEndpointTestCase(APITestCase):
    """Test cases for Pipeline endpoints"""
    authenticate = True
    status_code = status.HTTP_200_OK if authenticate else status.HTTP_403_FORBIDDEN
    super_user = 'super'
    regular_user = 'regular'

    def setUp(self):
        # Clear all pipeline objects and create initial pipeline
        Pipeline.objects.create(title='Test Pipeline', pk=1)  # type: ignore

        # Only create user accounts if not anonymous
        if self.authenticate:
            # Clear all user objects and create initial accounts
            User.objects.create_superuser(username=self.super_user, email='', password='', pk=1)
            User.objects.create_user(self.regular_user, email='', password='', pk=2)

    def login(self, regular=True):
        # Login as a superuser for each test, individual tests may override
        name = self.regular_user if regular else self.super_user
        self.client.login(username=name)

        # Get auth token
        data = {'username': name, 'password': "."}
        response = self.client.post("/users/obtain/", data=data, follow=True)
        return json.loads(response.content)['access']

    def test_pipelines_listview(self):
        """Test the pipelines listview endpoint"""
        token = self.login(regular=False)
        response = self.client.get("/pipelines/", HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_detailview(self):
        """Test the pipelines individal detail endpoint"""
        token = self.login()

        # Find the current pipeline and user
        pipeline: Pipeline = Pipeline.objects.all()[0]
        user: User = User.objects.filter(username=self.regular_user)[0]

        # Set the user as a manager and viewer of the pipeline
        Manager.objects.create(user=user, pipeline=pipeline)
        Viewer.objects.create(user=user, pipeline=pipeline)

        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.get(f'/pipelines/{pipeline_id}/',
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_updateview_get(self):
        """Test the pipelines get update endpoint"""
        token = self.login(regular=False)

        # Create and send request
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated"}
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.get(f'/pipelines/{pipeline_id}/', data=data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_updateview_manager_put(self):
        """Test the pipelines put update endpoint"""
        token = self.login()
        pipeline_id = Pipeline.objects.all()[0].pk
        Manager.objects.create(user=User.objects.get(username=self.regular_user),
                               pipeline=Pipeline.objects.get(pk=pipeline_id))
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated"}
        self.assertNotEquals(Pipeline.objects.count(), 0)

        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 0)

    def test_pipelines_updateview_uploader_put(self):
        """Test the pipelines put update endpoint"""
        # A request is only created if the user is not a manager or superuser
        pipeline: Pipeline = Pipeline.objects.all()[0]
        user: User = User.objects.filter(username=self.regular_user)[0]

        Uploader.objects.create(user=user, pipeline=pipeline)
        Viewer.objects.create(user=user, pipeline=pipeline)
        token = self.login()

        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated"}
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 1)

    def test_pipelines_history(self):
        """Test the pipelines get history"""
        token = self.login(regular=False)
        response = self.client.get("/pipelines/1/history/", HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
        self.assertEquals(response.status_code, self.status_code)
