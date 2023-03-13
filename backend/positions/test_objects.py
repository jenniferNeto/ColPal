from django.test import TestCase
from django.contrib.auth.models import User

from pipeline.models import Pipeline
from .models import Viewer


class PositionTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Pipeline.objects.all().delete()

        User.objects.create(username='Test User')
        Pipeline.objects.create(title='Test Pipeline')

    def test_position_create(self):
        """Test the creation of a Viewer object"""
        position_user = User.objects.all().first()
        position_pipeline = Pipeline.objects.all().first()

        viewer = Viewer.objects.create(user=position_user, pipeline=position_pipeline)
        self.assertEquals(Viewer.objects.all().count(), 1)

        user = viewer.user
        self.assertNotEquals(user, None)
        if user is not None:
            self.assertEquals(user.get_username(), 'Test User')

        pipeline = viewer.pipeline
        self.assertNotEquals(pipeline, None)
        if pipeline is not None:
            self.assertEquals(pipeline.title, 'Test Pipeline')
