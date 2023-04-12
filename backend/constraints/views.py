from rest_framework import generics
from rest_framework.response import Response

from django.http import Http404

from pipeline.models import Pipeline

from .models import Constraint
from .serializers import ConstraintSerializer, ConstraintUpdateSerializer

class ConstraintsListAPIView(generics.ListAPIView):
    serializer_class = ConstraintSerializer
    queryset = Constraint.objects.all()

    def get(self, request, pk_pipeline):
        # Verify pipeline exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404

        # Validate the serializer data
        instance = Constraint.objects.filter(pipeline=pipeline)
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(ConstraintSerializer(instance, many=True).data)


class ConstraintUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ConstraintUpdateSerializer
    queryset = Constraint.objects.all()

    def get(self, request, pk_pipeline, pk_constraint):
        # Verify pipeline and constraint exist
        try:
            Pipeline.objects.get(pk=pk_pipeline)
            constraint = Constraint.objects.get(pk=pk_constraint)
        except (Pipeline.DoesNotExist, Constraint.DoesNotExist):
            raise Http404

        # Validate the serializer data
        serializer = ConstraintSerializer(constraint, data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

    def put(self, request, pk_pipeline, pk_constraint):
        # Verify pipeline and constraint exist
        try:
            Pipeline.objects.get(pk=pk_pipeline)
            constraint = Constraint.objects.get(pk=pk_constraint)
        except (Pipeline.DoesNotExist, Constraint.DoesNotExist):
            raise Http404

        # Get new attribute from request and update object
        attribute = request.data['attribute_type']
        constraint.attribute_type = attribute

        # Validate update
        serializer = self.get_serializer(constraint, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Update object in database
        self.perform_update(serializer)

        return Response(serializer.data)
