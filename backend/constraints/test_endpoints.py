from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import User

from django.core.files.uploadedfile import SimpleUploadedFile

import json

from request.models import Request
from positions.models import Viewer, Uploader, Manager

from .models import Constraint

from pipeline.models import Pipeline, PipelineFile

import csv

class ConstraintValidaiton(APITestCase):
    """Test cases for all types of constraints"""

    def setUp(self):
        # Email and password don't matte rin this context but are required to create a superuser
        user = User.objects.create_superuser(username="test", email="", password="")
        pipeline = Pipeline.objects.create(title="Pipeline", is_approved=True)

        Manager.objects.create(user=user, pipeline=pipeline)

    def login(self):
        # Login as a superuser for each test, individual tests may override
        self.client.login(username="test")

        # Get auth token
        data = {'username': "test", 'password': "."}
        response = self.client.post("/users/obtain/", data=data, follow=True)
        return json.loads(response.content)['access']

    def test_constraints(self):
        token = self.login()

        # Define headers and get pipeline
        headers = ['Varchar', 'Integer', 'Float', 'Date', 'Boolean', 'Datetime', 'Email']
        pipeline = Pipeline.objects.get(title='Pipeline')

        # Write template file locally with created headers
        with open('template_file.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(headers)

        # File must be SimpleUploadedFile for django object
        file = open('template_file.csv', 'r')
        simple_file = SimpleUploadedFile('template_file.csv', bytes(file.read(), 'UTF-8'), content_type='text/csv')
        response = self.client.post(f"/pipelines/{pipeline.pk}/upload/",
                                    data={'file': simple_file},
                                    HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                    follow=True)

        # Validate status of uploaded file and close
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        file.close()

        # Write all test values to a file
        with open('test.csv', 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(headers)
            writer.writerow(['VALID', '1', '1.0', '04/09/2001', 'True', '04/09/2001:01:03:03', 'email@email.com'])

        # Generate the constraints for the pipeline
        pipeline_file = PipelineFile.objects.last()

        # Check uploaded file for None
        self.assertNotEquals(pipeline_file, None)

        [print("Constraint:", obj.pk) for obj in Constraint.objects.all()]

        # Check None for autocomplete
        if pipeline_file:
            # Make requests to set all header constraints
            for index in range(0, len(headers)):
                value = index + 1
                print("URL:", f"/pipeline/{pipeline.pk}/constraints/{value}/")
                response = self.client.put(f"/pipeline/{pipeline.pk}/constraints/{value}/",
                                           data={'attributes_type': value},
                                           HTTP_AUTHORIZATION='Bearer {}'.format(token),
                                           follow=True)

                print("Content:", response.content)
                print("Context:", response.context)
                self.assertEquals(response.status_code, status.HTTP_200_OK)

        # File must be SimpleUploadedFile for django object
        file = open('test.csv', 'r')
        simple_file = SimpleUploadedFile('test.csv', bytes(file.read(), 'UTF-8'), content_type='text/csv')
        response = self.client.get(f"/pipelines/{pipeline.pk}/", HTTP_AUTHORIZATION='Bearer {}'.format(token), follow=True)
