from django.test import TestCase, Client
from datetime import timedelta

from .models import Pipeline


class PipelineEndpointTestCase(TestCase):
    """
    Test cases for the creation and modification of Pipeline objects
    .all() warnings can be ignored
    """
    def setUp(self):
        Pipeline.objects.all().delete()
        Pipeline.objects.create(title='Test Pipeline')


    def test_pipelines_listview(self):
        """Test the pipelines listview endpoint"""
        client = Client()
        response = client.get('/pipelines/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_pipelines_detailview(self):
        """Test the individial pipelines view"""
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.get('/pipelines/1', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_pipelines_history(self):
        """Test the individial pipelines history"""
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.get('/pipelines/1/history', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_pipelines_update(self):
        """Test the individial pipelines history"""
        client = Client(HTTP_USER_AGENT='Mozilla/5.0')
        response = client.patch('/pipelines/1/update', {'title': "New Title"}, follow=True)
        self.assertEquals(response.status_code, 200)

    # Do same 405 error trick that worked with update serializers
    # def test_pipelines_create(self):
    #     """Test the individial pipelines history"""
    #     client = Client(HTTP_USER_AGENT='Mozilla/5.0')
    #     response = client.patch('/pipelines/1/update', {'title': "New Title"}, follow=True)
    #     self.assertEquals(response.status_code, 200)

    def test_pipelines_invalid_detailview(self):
        """Test the individial pipelines view"""
        client = Client()
        response = client.get('/pipelines/2', follow=True)
        self.assertEquals(response.status_code, 404)

    def test_pipeline_save_upload_frequency(self):
        """Test updating pipeline upload_frequency"""
        pipeline = Pipeline.objects.all()[0]
        pipeline.upload_frequency = timedelta(days=1)
        pipeline.save()

        self.assertEquals(pipeline.upload_frequency, timedelta(days=1))
        self.assertNotEquals(pipeline.last_modified, None)
        self.assertEquals(pipeline.history.all().count(), 2)

    def test_pipeline_save_is_approved(self):
        """Test updating pipeline is_approved"""
        pipeline = Pipeline.objects.all()[0]
        pipeline.is_approved = True
        pipeline.save()

        self.assertEquals(pipeline.is_approved, True)
        self.assertNotEquals(pipeline.last_modified, None)
        self.assertNotEquals(pipeline.approved_date, None)
        self.assertEquals(pipeline.history.all().count(), 2)

    def test_pipeline_save_is_active(self):
        """Test updating pipeline is_active"""
        pipeline = Pipeline.objects.all()[0]
        pipeline.is_active = False
        pipeline.save()

        self.assertEquals(pipeline.is_active, False)
        self.assertNotEquals(pipeline.last_modified, None)
        self.assertEquals(pipeline.history.all().count(), 2)
