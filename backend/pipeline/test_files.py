from rest_framework.test import APITestCase
from rest_framework import status

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
from django.contrib.auth.models import User
from django.utils import timezone

import json
import csv
import os

from request.models import Request
from positions.models import Viewer, Uploader, Manager

from .models import Pipeline, PipelineFile

class PipelineFileEndpointTestCase(APITestCase):
    """Test cases for Pipline files"""

    def setUp(self):
        # Email and password don't matter in this context but are required to create a superuser
        User.objects.create_superuser(username="test", email="", password="")
        Pipeline.objects.create(
            title='Test Pipeline',
            upload_frequency='10',
            is_approved=True, is_active=True,
            approved_date=timezone.now()
        )

    def login(self):
        # Login as a superuser for each test, individual tests may override
        self.client.login(username="test")

        # Get auth token
        data = {'username': "test", 'password': "."}
        response = self.client.post("/users/obtain/", data=data, follow=True)
        return json.loads(response.content)['access']

    def test_pipeline_file_upload(self):
        """Test pipelines can upload files"""
        token = self.login()

        # Get user and pipeline objects
        user = User.objects.get(username='test')
        pipeline = Pipeline.objects.get(title='Test Pipeline')

        # Make the user a upload to the pipeline
        Uploader.objects.create(user=user, pipeline=pipeline)

        # Create the text file
        with open('students.csv', 'w', newline='') as file:
            # Create file writer
            writer = csv.writer(file)

            # Write sample data to file
            writer.writerow(["Num", "FirstName", "LastName"])
            writer.writerow([1, "Shane", "Arcaro"])

            # File needs to be SimpleUploadedFile to work with Django
            csv_file = SimpleUploadedFile(name='students.csv', content=b"file_content", content_type='text/csv')

            response = self.client.post(f'/pipelines/{pipeline.pk}/upload/',
                                        HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                        data={'file': csv_file},
                                        follow=True)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f'/pipelines/{pipeline.pk}/files/',
                                   HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                   follow=True)

        # Verify pipeline file object was created and response was honored
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(PipelineFile.objects.count(), 1)

        # Verify file was uploaded to google cloud bucket
        self.assertEquals(len(json.loads(response.content)), 1)

        # Delete created file
        os.remove('students.csv')
