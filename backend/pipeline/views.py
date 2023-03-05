from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from django.http import Http404
from django.core.exceptions import PermissionDenied

from positions.models import Manager, Viewer

from request.utils import createRequest

from .models import Pipeline
from .serializers import PipelineSerializer, PipelineHistorySeralizer, PipelineUpdateSerializer


class PipelineListAPIView(generics.ListAPIView):
    """View all created pipelines"""
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    permission_classes = [IsAdminUser]

class ApprovedPipelineListAPIView(generics.ListAPIView):
    """View all created pipelines"""
    queryset = Pipeline.objects.filter(is_approved=True)
    serializer_class = PipelineSerializer
    permission_classes = [IsAdminUser]

class PipelineDetailAPIView(generics.RetrieveAPIView):
    """View a specific pipeline based on its id"""
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

class PipelineCreateAPIView(generics.CreateAPIView):
    """Create a new pipeline"""
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PipelineUpdateAPIView(generics.UpdateAPIView):
    """Update a pipeline"""
    queryset = Pipeline.objects.all()
    serializer_class = PipelineUpdateSerializer

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, args, kwargs)

    def put(self, request, *args, **kwargs):
        pipeline_id = self.kwargs['pk']
        # Query the most recent updated model of the history
        # If history is queried then updated the query will be off by one
        instance = Pipeline.objects.filter(pk=pipeline_id).first()

        return self.create(request, instance=instance)
        # # Check to see if user is allowed to update this pipeline
        # self.check_user_permissions(request, pipeline_id)

        # # Set update_reason to None so it becomes a required field
        # pipeline.update_reason = None

        # # Perform super update with modified instance
        # # super.update() will pull pipeline instance without additional field
        # partial = kwargs.pop('partial', False)
        # serializer = self.get_serializer(instance, data=request.data, partial=partial)
        # serializer.is_valid(raise_exception=True)
        # self.perform_update(serializer)

        # # Update change reason in history on model
        # update_request = request.data["update_reason"]
        # update_change_reason(pipeline, update_request)

        # return Response(serializer.data)

    def create(self, request, instance):
        if instance is None:
            raise Http404

        serializer = self.get_serializer(instance, data=request.data)
        instance.update_reason = None
        serializer.is_valid(raise_exception=True)

        # Create the new request object
        createRequest(data=request.data, instance=instance)

        return Response(status=status.HTTP_200_OK)

    def get(self, request, pk):
        pipeline = Pipeline.objects.filter(pk=pk).first()
        if pipeline is None:
            raise Http404

        # Check to see if a user is allowed to update this pipeline
        self.check_user_permissions(request, pk)

        # Set update_reason to None so PipelineUpdateSerializer can
        # match all the required added fields on a Pipeline
        # Without this line update requests will always be 405 response code
        pipeline.update_reason = None
        return Response(PipelineSerializer(pipeline).data)

    def check_user_permissions(self, request, pk):
        """
        TODO: Update later for Uploader permissions
        Temporary permission checking to demonstate how it will work
        """
        # Get current user instance
        user = request.user

        # Get managers for the current pipeline
        managers = Manager.objects.filter(pipeline_id=pk).values_list('user', flat=True)

        if not user.is_staff and user not in managers:
            raise PermissionDenied

class PipelineHistoricalRecordsRetrieveAPIView(generics.ListAPIView):
    """View pipeline historical instances"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        pipeline = Pipeline.objects.filter(pk=pipeline_id)

        # Check if pipeline exists
        if pipeline.count() == 0:
            raise Http404
        return pipeline

    serializer_class = PipelineHistorySeralizer
