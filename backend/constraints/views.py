from rest_framework import generics, status
from rest_framework.response import Response

from django.http import Http404

from pipeline.models import Pipeline, PipelineFile

from .models import Constraint
from .serializers import ConstraintSerializer

class ConstraintsListAPIView(generics.ListAPIView):
    serializer_class = ConstraintSerializer
    queryset = Constraint.objects.all()

    def get(self, request, pk_pipeline, pk_pipelinefile):
        # Verify pipeline exists
        try:
            Pipeline.objects.get(pk=pk_pipeline)
            pipeline_file = PipelineFile.objects.get(pk=pk_pipelinefile)
        except (Pipeline.DoesNotExist, PipelineFile.DoesNotExist):
            raise Http404

        # Validate the serializer data
        instance = Constraint.objects.filter(pipeline_file=pipeline_file)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(ConstraintSerializer(instance, many=True).data)
