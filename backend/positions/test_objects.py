from django.test import TestCase
from django.contrib.auth.models import User

from pipeline.models import Pipeline
from .models import Viewer, Uploader, Manager


class ViewerTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Pipeline.objects.all().delete()

        User.objects.create(username='Test User')
        Pipeline.objects.create(title='Test Pipeline')

    def test_viewer_create(self):
        """Test the creation of a Viewer object"""
        user = User.objects.all()[0]
        pipeline = Pipeline.objects.all()[0]

        viewer = Viewer.objects.create(viewer=user, pipeline=pipeline)
        self.assertEquals(Viewer.objects.all().count(), 1)

        viewer_viewer = viewer.viewer
        self.assertNotEquals(viewer_viewer, None)
        if viewer_viewer is not None:
            self.assertEquals(viewer_viewer.get_username(), 'Test User')

        viewer_pipeline = viewer.pipeline
        self.assertNotEquals(viewer_pipeline, None)
        if viewer_pipeline is not None:
            self.assertEquals(viewer_pipeline.title, 'Test Pipeline')

class UploaderTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Pipeline.objects.all().delete()

        User.objects.create(username='Test User')
        Pipeline.objects.create(title='Test Pipeline')

    def test_uploader_create(self):
        """Test the creation of a Uploader object"""
        user = User.objects.all()[0]
        pipeline = Pipeline.objects.all()[0]

        uploader = Uploader.objects.create(uploader=user, pipeline=pipeline)
        self.assertEquals(Uploader.objects.all().count(), 1)

        uploader_uploader = uploader.uploader
        self.assertNotEquals(uploader_uploader, None)
        if uploader_uploader is not None:
            self.assertEquals(uploader_uploader.get_username(), 'Test User')

        uploader_pipeline = uploader.pipeline
        self.assertNotEquals(uploader_pipeline, None)
        if uploader_pipeline is not None:
            self.assertEquals(uploader_pipeline.title, 'Test Pipeline')

class ManagerTestCase(TestCase):
    def setUp(self):
        User.objects.all().delete()
        Pipeline.objects.all().delete()

        User.objects.create(username='Test User')
        Pipeline.objects.create(title='Test Pipeline')

    def test_manager_create(self):
        """Test the creation of a Manager object"""
        user = User.objects.all()[0]
        pipeline = Pipeline.objects.all()[0]

        manager = Manager.objects.create(manager=user, pipeline=pipeline)
        self.assertEquals(Manager.objects.all().count(), 1)

        manager_manager = manager.manager
        self.assertNotEquals(manager_manager, None)
        if manager_manager is not None:
            self.assertEquals(manager_manager.get_username(), 'Test User')

        manager_pipeline = manager.pipeline
        self.assertNotEquals(manager_pipeline, None)
        if manager_pipeline is not None:
            self.assertEquals(manager_pipeline.title, 'Test Pipeline')
