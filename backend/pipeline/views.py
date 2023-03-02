from rest_framework import generics

from .models import Pipeline, ModificationPipelineRequest
from .serializers import PipelineSerializer, PipelineHistorySeralizer

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


class PipelineRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Update a pipeline
    """

    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

    def update(self, request, *args, **kwargs):
        """
        This is broken. Currently when the user updates a model
        a new empty Pipeline is created
        """
        # request_data = json.loads(request.raw_post_data)

        partial = kwargs.pop('partial', False)
        instance: Pipeline = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        update_request = super().update(request)

        previousInstance: Pipeline = Pipeline.objects.get(pk=instance.pk)

        mod = ModificationPipelineRequest.objects.create()

        """
        Need someway to update the model only after it has been approved
        by either a manager or an admin. The user should request an update
        and it should not immediately be accepted by the system.
        """

        print("===================================", previousInstance.__dict__)
        print("===================================", mod.__dict__)
        return update_request

class PipelineHistoricalRecordsRetrieveAPIView(generics.ListAPIView):
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Pipeline.objects.filter(pk=pipeline_id)

    serializer_class = PipelineHistorySeralizer
