from rest_framework import generics

from django.core import exceptions

from .models import Viewer, Uploader, Manager
from .seralizers import ViewerSerailizer, UploaderSerailizer, ManagerSerailizer

class ViewerRetrieveAPIView(generics.ListAPIView):
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Viewer.objects.filter(pipeline_id=pipeline_id)

    serializer_class = ViewerSerailizer

class UploaderRetrieveAPIView(generics.ListAPIView):
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Uploader.objects.filter(pipeline_id=pipeline_id)

    serializer_class = UploaderSerailizer

class ManagerRetrieveAPIView(generics.ListAPIView):
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Manager.objects.filter(pipeline_id=pipeline_id)

    serializer_class = ManagerSerailizer
