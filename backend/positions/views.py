from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

from pipeline.models import Pipeline
from authentication.utils import check_user_permissions

from .models import Viewer, Uploader, Manager
from . import serializers

User = get_user_model()


class IsViewerRequired(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        check_user_permissions(request, kwargs['pk_pipeline'], Manager)
        return super().get(request, *args, **kwargs)

class ViewerListAPIView(IsViewerRequired):
    """View all Viewers for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Viewer.objects.filter(pipeline_id=pipeline_id)

    serializer_class = serializers.ViewerSerializer

class UploaderListAPIView(IsViewerRequired):
    """View all Uploaders for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Uploader.objects.filter(pipeline_id=pipeline_id)

    serializer_class = serializers.UploaderSerializer

class ManagerListAPIView(IsViewerRequired):
    """View all Managers for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Manager.objects.filter(pipeline_id=pipeline_id)

    serializer_class = serializers.ManagerSerializer

class ViewerCreateAPIView(generics.CreateAPIView):
    """Create a new viewer for a specific pipeline"""
    queryset = Viewer.objects.none()
    serializer_class = serializers.ViewerCreateSerializer

    def post(self, request, pk_pipeline):
        # Check user is a manager
        check_user_permissions(request, pk_pipeline, Manager)

        user = User.objects.filter(pk=request.data['id']).first()
        pipeline = Pipeline.objects.filter(pk=pk_pipeline).first()

        # Attempt to create a Viewer on the pipeline which requires a unique instance
        try:
            Viewer.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            raise ValidationError(detail='User is already a viewer of this pipeline')

        return Response(request.data)

class UploaderCreateAPIView(generics.CreateAPIView):
    """Create a new viewer for a specific pipeline"""
    queryset = Uploader.objects.none()
    serializer_class = serializers.UploaderCreateSerializer

    def post(self, request, pk_pipeline):
        # Check user is a manager
        check_user_permissions(request, pk_pipeline, Manager)

        user = User.objects.filter(pk=request.data['id']).first()
        pipeline = Pipeline.objects.filter(pk=pk_pipeline).first()

        # Attempt to create a Uploader on the pipeline which requires a unique instance
        try:
            Uploader.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            raise ValidationError(detail='User is already a uploader of this pipeline')

        # Managers are automatically viewers of a pipeline
        try:
            Viewer.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            pass

        return Response(request.data)

class ManagerCreateAPIView(generics.CreateAPIView):
    """Create a new viewer for a specific pipeline"""
    queryset = Uploader.objects.none()
    serializer_class = serializers.ManagerCreateSerializer

    def post(self, request, pk_pipeline):
        # Check user is a manager
        check_user_permissions(request, pk_pipeline, Manager)

        user = User.objects.filter(pk=request.data['id']).first()
        pipeline = Pipeline.objects.filter(pk=pk_pipeline).first()

        # Attempt to create a Manager on the pipeline which requires a unique instance
        try:
            Manager.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            raise ValidationError(detail='User is already a manager of this pipeline')

        # Managers are automatically viewers of a pipeline
        try:
            Viewer.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            pass

        return Response(request.data)
