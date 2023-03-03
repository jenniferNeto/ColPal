from rest_framework import generics
from simple_history.utils import update_change_reason
from django.http import Http404

from .models import Pipeline, ModificationPipelineRequest
from .serializers import PipelineSerializer, PipelineHistorySeralizer, PipelineUpdateSerializer

class PipelineListAPIView(generics.ListAPIView):
    """
    View all created pipelines
    """
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

class ApprovedPipelineListAPIView(generics.ListAPIView):
    """
    View all created pipelines
    """
    queryset = Pipeline.objects.filter(is_approved=True)
    serializer_class = PipelineSerializer

class PipelineDetailAPIView(generics.RetrieveAPIView):
    """
    View a specific pipeline based on its id
    """
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

class PipelineCreateAPIView(generics.CreateAPIView):
    """
    Create a new pipeline
    """
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer


class PipelineUpdateAPIView(generics.UpdateAPIView):
    """
    Update a pipeline
    """
    queryset = Pipeline.objects.all()
    serializer_class = PipelineUpdateSerializer

    def get_queryset(self):
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        # Perform the update on the current model first
        update_model = super().update(request)

        pipeline_id = self.kwargs['pk']
        # Query the most recent updated model of the history
        # If history is queried then updated the query will be off by one
        pipeline = Pipeline.objects.filter(pk=pipeline_id)[0]

        # Update change reason in history on model
        update_request = request.data["update_reason"]
        update_change_reason(pipeline, update_request)

        return update_model


class PipelineHistoricalRecordsRetrieveAPIView(generics.ListAPIView):
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        pipeline = Pipeline.objects.filter(pk=pipeline_id)

        # Check if pipeline exists
        if pipeline.count() == 0:
            raise Http404
        return pipeline

    serializer_class = PipelineHistorySeralizer
