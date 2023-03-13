from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

from request.models import Request
from positions.models import Viewer, Uploader, Manager

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
        response = self.client.get("/pipelines/0/", follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_updateview_get_invalid(self):
        """Test non-existant pipeline update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        response = self.client.get("/pipelines/0/update/", data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_pipelines_updateview_put_invalid_upload_frequency(self):
        """Test the pipelines put update endpoint invalid upload frequency"""
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        data = {'title': "Title", 'upload_frequency': "e", 'update_reason': "Updated", 'is_active': True}
        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)  # error 200 != 400

    def test_pipelines_updateview_put_invalid_update_reason(self):
        """Test the pipelines put update endpoint invalid update_reason"""
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        data = {'title': "Title", 'upload_frequency': "0", 'is_active': True}
        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data, follow=True)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)  # error 200 != 400

    def test_pipelines_history_invalid(self):
        """Test the pipelines get history"""
        response = self.client.get("/pipelines/0/history/", follow=True)
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
        # Clear all pipeline objects and create initial pipeline
        Pipeline.objects.all().delete()
        Pipeline.objects.create(title='Test Pipeline', pk=1)

        # Clear all request objects
        Request.objects.all().delete()

        # Only create user accounts if not anonymous
        if self.authenticate:
            # Clear all user objects and create initial accounts
            User.objects.all().delete()
            superuser = User.objects.create_superuser(username='super', email='', password='', pk=1)
            User.objects.create_user('regular', email='', password='', pk=2)

            # Login as a superuser for each test, individual tests may override
            self.client.login(username=superuser.username)

    def test_pipelines_listview(self):
        """Test the pipelines listview endpoint"""
        response = self.client.get("/pipelines/", follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_detailview(self):
        """Test the pipelines individal detail endpoint"""
        if self.authenticate:
            # Find the current pipeline and user
            pipeline: Pipeline = Pipeline.objects.all()[0]
            user: User = User.objects.filter(username="super")[0]

            # Set the user as a manager and viewer of the pipeline
            Manager.objects.create(user=user, pipeline=pipeline)
            Viewer.objects.create(user=user, pipeline=pipeline)

        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.get(f'/pipelines/{pipeline_id}/', follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_updateview_get(self):
        """Test the pipelines get update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.get(f'/pipelines/{pipeline_id}/', data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)

    def test_pipelines_updateview_manager_put(self):
        """Test the pipelines put update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 0)

    def test_pipelines_updateview_uploader_put(self):
        """Test the pipelines put update endpoint"""
        # A request is only created if the user is not a manager or superuser
        self.client.logout()
        if self.authenticate:
            pipeline: Pipeline = Pipeline.objects.all()[0]
            user: User = User.objects.filter(username="regular")[0]

            Uploader.objects.create(user=user, pipeline=pipeline)
            Viewer.objects.create(user=user, pipeline=pipeline)
            self.client.login(username=user.username)

        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 1)

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
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 0)

    def test_pipelines_updateview_uploader_put(self):
        """Test the pipelines put update endpoint"""
        data = {'title': "Title", 'upload_frequency': "00:00:10", 'update_reason': "Updated", 'is_active': True}
        self.assertNotEquals(Pipeline.objects.count(), 0)
        pipeline_id = Pipeline.objects.all()[0].pk
        response = self.client.put(f'/pipelines/{pipeline_id}/update/', data=data, follow=True)
        self.assertEquals(response.status_code, self.status_code)
        self.assertEquals(Request.objects.all().count(), 0)
