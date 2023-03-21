from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

import json

from positions.models import Viewer, Uploader, Manager
from pipeline.models import Pipeline

from .models import Request


class RequestEndpointTestCase(APITestCase):
    """Test cases for Requests"""
    super_user = 'super'
    regular_user = 'regular'

    def setUp(self):
        # Clear all pipeline objects and create initial pipeline
        Pipeline.objects.create(title='Test Pipeline', pk=1)

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

    def make_update_request(self, regular=True):
        token = self.login(regular=regular)

        # Get pipeline information
        pipeline = Pipeline.objects.all()[0]
        pipeline_id = pipeline.pk
        self.assertNotEquals(pipeline, None)

        # Add user as uploader and viewer to pipeline if regular
        if regular:
            Viewer.objects.create(user=User.objects.get(username='regular' if regular else 'super'), pipeline=pipeline)
            Uploader.objects.create(user=User.objects.get(username='regular' if regular else 'super'),
                                    pipeline=pipeline)

        # Send pipeline update request
        data = {'title': 'New title', 'upload_frequency': 100, 'is_active': True, 'update_reason': 'Test'}
        self.client.put(f'/pipelines/{pipeline_id}/update/', data=data,
                        HTTP_AUTHORIZATION='Bearer {}'.format(token),
                        follow=True)
        return token, pipeline

    def test_pipeline_manager_request_accept(self):
        """Test that a manager can accept a pipeline"""
        token, pipeline = self.make_update_request()

        # Get the request object and add user as a manager
        request = Request.objects.all().last()
        if request is None:
            self.assertNotEqual(request, None)
            return

        Manager.objects.create(user=User.objects.get(username='regular'), pipeline=pipeline)

        # View requests page
        response = self.client.get(f'/pipelines/requests/{request.pk}/',
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                   follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Approve request
        data = {'accept_changes': "1", 'response': "Sure"}
        response = self.client.put(f'/pipelines/requests/{request.pk}/', data=data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                   follow=True)

        # Check 200 response status of HTTPRequest and if request object was created
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_pipeline_admin_request_accept(self):
        """Test that an admin can accept a pipeline it's not a manager of"""
        self.make_update_request()

        # Login as super user
        token = self.login(regular=False)

        # Get request
        request = Request.objects.all().last()
        if request is None:
            self.assertNotEqual(request, None)
            return

        # View requests page
        response = self.client.get(f'/pipelines/requests/{request.pk}/',
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                   follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        # Approve request
        data = {'accept_changes': 1, 'response': 'Sure'}
        response = self.client.put(f'/pipelines/requests/{request.pk}/', data=data,
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                   follow=True)

        # Check 200 response status of HTTPRequest and if request object was created
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    # def test_pipeline_request_accept(self):
    #     """Test that the updated pipeline actually updated"""
    #     _, pipeline = self.make_update_request()

    #     # Get login token
    #     token = self.login(regular=False)

    #     # Get request
    #     request = Request.objects.all().last()
    #     if request is None:
    #         self.assertNotEqual(request, None)
    #         return

    #     # Approve request
    #     data = {'accept_changes': 1, 'response': 'Sure'}
    #     response = self.client.put(f'/pipelines/requests/{request.pk}/', data=data,
    #                                HTTP_AUTHORIZATION='Bearer {}'.format(token),
    #                                follow=True)
    #     self.assertEquals(response.status_code, status.HTTP_200_OK)

    #     self.assertEquals(pipeline.title, 'New title')
    #     self.assertEquals(pipeline.upload_frequency, 100)
    #     self.assertEquals(pipeline.is_active, True)

    """
    Make unit tests specifically testing the feature that only adds
    the attributes when they are being altered in the requests.
    """
