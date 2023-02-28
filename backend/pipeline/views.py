from rest_framework import generics

from .models import Pipeline
from .serializers import PipelineSerializer


class PipelineListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

class PipelineDetailAPIView(generics.RetrieveAPIView):
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
