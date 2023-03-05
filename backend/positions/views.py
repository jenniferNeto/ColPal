from rest_framework import generics

from .models import Viewer, Uploader, Manager
from .seralizers import ViewerSerializer, UploaderSerializer, ManagerSerializer

class ViewerListAPIView(generics.ListAPIView):
    """View all Viewers for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Viewer.objects.filter(pipeline_id=pipeline_id)

    serializer_class = ViewerSerializer

class UploaderListAPIView(generics.ListAPIView):
    """View all Uploaders for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Uploader.objects.filter(pipeline_id=pipeline_id)

    serializer_class = UploaderSerializer

class ManagerListAPIView(generics.ListAPIView):
    """View all Managers for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Manager.objects.filter(pipeline_id=pipeline_id)

    serializer_class = ManagerSerializer
