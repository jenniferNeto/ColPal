from django.test import TestCase
from datetime import timedelta

from .models import Pipeline


class PipelineTestCase(TestCase):
    """
    Test cases for the creation and modification of Pipeline objects
    .all() warnings can be ignored
    """
    def setUp(self):
        Pipeline.objects.all().delete()  # type: ignore
        Pipeline.objects.create(title='Test Pipeline')

    def test_pipeline_create(self):
        """Test the creation of a Pipeline object"""
        pipeline = Pipeline.objects.all()[0]

        self.assertEquals(pipeline.title, 'Test Pipeline')
        self.assertEquals(pipeline.upload_frequency, timedelta(0))
        self.assertEquals(pipeline.is_approved, False)
        self.assertEquals(pipeline.is_active, True)
        self.assertEquals(pipeline.approved_date, None)
        self.assertEquals(pipeline.history.all().count(), 1)  # type: ignore

    def test_pipeline_save_title(self):
        """Test updating Pipeline title"""
        pipeline = Pipeline.objects.all()[0]
        pipeline.title = 'New Title'
        pipeline.save()

        self.assertEquals(pipeline.title, 'New Title')
        self.assertNotEquals(pipeline.last_modified, None)
        self.assertEquals(pipeline.history.all().count(), 2)  # type: ignore

    def test_pipeline_save_upload_frequency(self):
        """Test updating pipeline upload_frequency"""
        pipeline = Pipeline.objects.all()[0]
        pipeline.upload_frequency = timedelta(days=1)
        pipeline.save()

        self.assertEquals(pipeline.upload_frequency, timedelta(days=1))
        self.assertNotEquals(pipeline.last_modified, None)
        self.assertEquals(pipeline.history.all().count(), 2)  # type: ignore

    def test_pipeline_save_is_approved(self):
        """Test updating pipeline is_approved"""
        pipeline = Pipeline.objects.all()[0]
        pipeline.is_approved = True
        pipeline.save()

        self.assertEquals(pipeline.is_approved, True)
        self.assertNotEquals(pipeline.last_modified, None)
        self.assertNotEquals(pipeline.approved_date, None)
        self.assertEquals(pipeline.history.all().count(), 2)  # type: ignore

    def test_pipeline_save_is_active(self):
        """Test updating pipeline is_active"""
        pipeline = Pipeline.objects.all()[0]
        pipeline.is_active = False
        pipeline.save()

        self.assertEquals(pipeline.is_active, False)
        self.assertNotEquals(pipeline.last_modified, None)
        self.assertEquals(pipeline.history.all().count(), 2)  # type: ignore
