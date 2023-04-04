from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ViewSet

from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from simple_history.utils import update_change_reason

from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

from authentication.utils import check_user_permissions, is_user_allowed
from positions.models import Viewer, Uploader, Manager
from request.utils import createRequest

from django.utils import timezone

from .models import Pipeline, PipelineFile
from .serializers import (
    PipelineSerializer,
    PipelineStatusSerializer,
    PipelineHistorySeralizer,
    PipelineUpdateSerializer,
    FileUploadSerializer
)

Users = get_user_model()


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

    def get(self, request, pk_pipeline):
        pipeline = Pipeline.objects.filter(pk=pk_pipeline).first()
        if pipeline is None:
            raise Http404
        # Check to see if a user is allowed to update this pipeline
        check_user_permissions(request, pk_pipeline, Viewer)

        # Set update_reason to None so PipelineUpdateSerializer can
        # match all the required added fields on a Pipeline
        # Without this line update requests will always be 405 response code
        pipeline.update_reason = None  # type: ignore
        return Response(PipelineSerializer(pipeline).data)

class PipelineCreateAPIView(generics.CreateAPIView):
    """Create a new pipeline"""
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer

    def create(self, request, *args, **kwargs):
        # Override create but with a different instance
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pipeline = serializer.save()
        headers = self.get_success_headers(serializer.data)

        # Whoever creates a pipeline is automatically a viewer and manager of that pipeline
        Manager.objects.create(user=request.user, pipeline=pipeline)
        Uploader.objects.create(user=request.user, pipeline=pipeline)
        Viewer.objects.create(user=request.user, pipeline=pipeline)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PipelineUpdateAPIView(generics.UpdateAPIView):
    """Update a pipeline"""
    queryset = Pipeline.objects.all()
    serializer_class = PipelineUpdateSerializer

    def put(self, request, *args, **kwargs):
        pipeline_id = self.kwargs['pk_pipeline']
        # Query the most recent updated model of the history
        # If history is queried then updated the query will be off by one
        instance = Pipeline.objects.filter(pk=pipeline_id).first()

        if instance is None:
            return Response(status.HTTP_404_NOT_FOUND)

        # User is manager and doesn't need to create an update request
        if is_user_allowed(request, pipeline_id, Manager):
            return self.perform_update_now(request, pipeline_id)

        # User must be an uploader to request changes to a pipeline
        check_user_permissions(request, pipeline_id, Uploader)

        return self.create(request, instance=instance)

    def perform_update_now(self, request, pipeline_id):
        instance = Pipeline.objects.filter(pk=pipeline_id)[0]
        # Set update_reason to None so it becomes a required field
        instance.update_reason = None  # type: ignore

        # Perform super update with modified instance
        # super.update() will pull pipeline instance without additional field
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update change reason in history on model
        update_reason = request.data["update_reason"]
        update_change_reason(instance, update_reason)

        return Response(serializer.data)

    def create(self, request, instance):
        if instance is None:
            raise Http404

        # Try a new request and check data integrity
        serializer = self.get_serializer(instance, data=request.data)
        instance.update_reason = None
        serializer.is_valid(raise_exception=True)

        # Create the new request object
        createRequest(data=request.data, instance=instance)

        return Response(status=status.HTTP_200_OK)

    def get(self, request, pk_pipeline):
        # Get pipeline and check if instance exists
        pipeline = Pipeline.objects.filter(pk=pk_pipeline).first()
        if pipeline is None:
            raise Http404

        # Check to see if a user is allowed to update this pipeline
        check_user_permissions(request, pk_pipeline, Uploader)

        # Set update_reason to None so PipelineUpdateSerializer can
        # match all the required added fields on a Pipeline
        # Without this line update requests will always be 405 response code
        pipeline.update_reason = None  # type: ignore
        return Response(PipelineSerializer(pipeline).data)

class PipelineStatusAPIView(generics.ListAPIView):
    """View pipeline approval status"""
    serializer_class = PipelineStatusSerializer

    def get(self, request, pk_pipeline):
        check_user_permissions(request, pk_pipeline, Manager)
        pipeline = Pipeline.objects.get(pk=pk_pipeline)

        # Check pipeline
        if not pipeline:
            raise Http404

        return Response(status=status.HTTP_200_OK, data={'approved': pipeline.is_approved})

    def put(self, request, pk_pipeline):
        pipeline = Pipeline.objects.get(pk=pk_pipeline)
        user = User.objects.get(pk=int(request.user.pk))

        # User needs to be admin to update the approval status of a pipeline
        if not user.is_superuser:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={
                    'message': 'Must be an admin to update the status'
                }
            )

        # Check pipeline
        if not pipeline:
            raise Http404

        approval_status = request.POST.get('approved')

        # Update pipeline
        pipeline.is_approved = bool(approval_status)
        pipeline.save()

        return Response(status=status.HTTP_200_OK, data={'id': pk_pipeline, 'approved': pipeline.is_approved})

class PipelineHistoricalRecordsRetrieveAPIView(generics.ListAPIView):
    """View pipeline historical instances"""
    serializer_class = PipelineHistorySeralizer

    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        pipeline = Pipeline.objects.filter(pk=pipeline_id)

        # Check if pipeline exists
        if pipeline.count() == 0:
            raise Http404
        return pipeline

    def get(self, request, *args, **kwargs):
        check_user_permissions(request, kwargs['pk_pipeline'], Viewer)
        return super().get(request, *args, **kwargs)

class UserPipelinesListAPIView(generics.ListAPIView):
    """View pipelines a user can upload to"""
    serializer_class = PipelineSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        uploaders = Uploader.objects.filter(user__pk=pk).values_list('pipeline_id')
        pipeline_ids = [pipe[0] for pipe in uploaders]
        return Pipeline.objects.filter(pk__in=pipeline_ids)

    def get(self, request, pk):
        # Get the user reference
        searched_user = User.objects.filter(pk=pk)

        # Check if user exists
        if searched_user.count() == 0:
            raise Http404
        user: User = searched_user[0]

        # Check if logged in user is admin
        if not request.user.is_superuser:
            # Check if requested user does not equal logged in user
            if not (user == request.user):
                return Response(status=status.HTTP_403_FORBIDDEN)
        return super().get(request)

class PipelineFileUpload(generics.CreateAPIView):
    """Upload files to an active and approved pipeline"""
    serializer_class = FileUploadSerializer

    def create(self, request, pk_pipeline):
        # Check to see if a user is allowed to update this pipeline
        check_user_permissions(request, pk_pipeline, Uploader)

        # Get the uploaded file from the request
        file = request.FILES.get('file')
        pipeline = Pipeline.objects.get(pk=pk_pipeline)

        # User can only upload files if pipeline is active and approved
        if not (pipeline.is_active and pipeline.is_approved):
            return Response(
                status=status.HTTP_403_FORBIDDEN,
                data={
                    'message': 'Pipeline must be approved and active to upload files'
                }
            )

        # Generate path to store file
        target_path = f'pipeline/{pk_pipeline}/{str(timezone.now().replace(tzinfo=None))}/{file}'
        saved_location = storage.save(target_path, file)

        # Connect uploaded file to pipeline using intermediary model
        pipeline_file = PipelineFile.objects.create(pipeline=pipeline, file=file, path=saved_location)

        # Get the date of the last uploaded file to the current pipeline
        latest_upload = PipelineFile.objects.filter(pipeline=pipeline).last()
        start_date = pipeline.created if latest_upload is None else latest_upload.upload_date

        # Calculate if the file is overdue and generate response data
        past_due = start_date + pipeline.upload_frequency < timezone.now()
        data = {
            'pipeline_id': pk_pipeline,
            'upload_date': pipeline_file.upload_date,
            'past_due': past_due,
            'filename': str(file),
            'file': saved_location
        }

        return Response(status=status.HTTP_201_CREATED, data=data)
