from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.http import Http404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils import timezone

from simple_history.utils import update_change_reason

from storages.backends.gcloud import GoogleCloudStorage
storage = GoogleCloudStorage()

from authentication.utils import check_user_permissions, is_user_allowed
from positions.models import Viewer, Uploader, Manager
from request.utils import create_pipeline_request
from constraints.utils import map_to_constraint
from constraints.models import Constraint

from .utils import is_stable, get_deadline
from .validators import generate_types, validate
from .models import Pipeline, PipelineFile, PipelineNotification
import pipeline.serializers as serializers

Users = get_user_model()


class PipelineListAPIView(generics.ListAPIView):
    """View all created pipelines"""
    queryset = Pipeline.objects.all()
    serializer_class = serializers.PipelineSerializer
    permission_classes = [IsAdminUser]

class ApprovedPipelineListAPIView(generics.ListAPIView):
    """View all created pipelines"""
    queryset = Pipeline.objects.filter(is_approved=True)
    serializer_class = serializers.PipelineSerializer
    permission_classes = [IsAdminUser]

class PipelineDetailAPIView(generics.RetrieveAPIView):
    """View a specific pipeline based on its id"""
    queryset = Pipeline.objects.all()
    serializer_class = serializers.PipelineSerializer

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
        return Response(serializers.PipelineSerializer(pipeline).data)

class PipelineCreateAPIView(generics.CreateAPIView):
    """Create a new pipeline"""
    queryset = Pipeline.objects.all()
    serializer_class = serializers.PipelineSerializer

    def create(self, request, *args, **kwargs):
        # Override create but with a different instance
        data = request.data.copy()
        # Remove constraints for serializer
        if 'constraints' in data:
            data.pop('constraints')

        pipeline_serializer = serializers.PipelineSerializer(data=data)
        constraints_serializer = serializers.ConstraintSerializer(data=request.data.get('constraints', []), many=True)
        pipeline_serializer.is_valid(raise_exception=True)
        pipeline = pipeline_serializer.save()

        # Generate constraints if found with request
        if request.data.get('constraints', []):
            constraints_serializer.is_valid(raise_exception=True)
            attribute_data = constraints_serializer.data

            for constraint in attribute_data:
                constraint['column_type'] = map_to_constraint(constraint['column_type'])
                Constraint.objects.create(
                    pipeline=pipeline,
                    column_title=constraint['column_name'],
                    column_type=constraint['column_type']
                )

        # Whoever creates a pipeline is automatically a viewer and manager of that pipeline
        Manager.objects.create(user=request.user, pipeline=pipeline)
        Uploader.objects.create(user=request.user, pipeline=pipeline)
        Viewer.objects.create(user=request.user, pipeline=pipeline)

        return Response(pipeline_serializer.data, status=status.HTTP_201_CREATED)

class PipelineUpdateAPIView(generics.UpdateAPIView):
    """Update a pipeline"""
    queryset = Pipeline.objects.all()
    serializer_class = serializers.PipelineUpdateSerializer

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
        create_pipeline_request(request=request, data=request.data, instance=instance)

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
        return Response(serializers.PipelineSerializer(pipeline).data)

class PipelineStatusAPIView(generics.RetrieveUpdateAPIView):
    """View pipeline approval status"""
    serializer_class = serializers.PipelineStatusSerializer

    def get(self, request, pk_pipeline):
        # Check to make sure pipeline exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404

        # Check user has permissions to view status
        check_user_permissions(request, pk_pipeline, Viewer)
        return Response(serializers.PipelineStatusSerializer(pipeline).data)

    def put(self, request, pk_pipeline):
        # Check to make sure pipeline exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404

        # Get user object
        user = User.objects.get(pk=int(request.user.pk))

        # User needs to be admin to update the approval status of a pipeline
        if not user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED, data={'detail': "Must be an admin account"})

        # Check pipeline
        if not pipeline:
            raise Http404

        # Get and update pipeline status
        approval_status = bool(request.POST.get('approved'))

        # If pipeline was approved with this request
        if not pipeline.is_approved and approval_status:
            pipeline.approved_date = timezone.now()

        # Update approval status and save
        pipeline.is_approved = approval_status
        pipeline.save()

        return Response(status=status.HTTP_200_OK, data={'id': pk_pipeline, 'approved': pipeline.is_approved})

class PipelineHistoricalRecordsRetrieveAPIView(generics.ListAPIView):
    """View pipeline historical instances"""
    serializer_class = serializers.PipelineHistorySeralizer

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
    serializer_class = serializers.PipelineSerializer

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

class PipelineFileUploadAPIView(generics.CreateAPIView):
    """Upload files to an approved pipeline"""
    serializer_class = serializers.FileUploadSerializer

    def create(self, request, pk_pipeline):
        # Check to make sure pipeline exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404

        # Check to see if a user is allowed to update this pipeline
        check_user_permissions(request, pk_pipeline, Uploader)

        # Get the uploaded file from the request
        file = request.FILES.get('file')

        """Pipeline is stable instead of active"""
        # # User can only upload files if pipeline is active and approved
        # if not (pipeline.is_active and pipeline.is_approved):
        #     return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': "Pipeline must be active and approved"})
        if not pipeline.is_approved:
            return Response(status=status.HTTP_403_FORBIDDEN,
                            data={'detail': "Pipeline must be approved by an admin before uploading files."})
        # Generate path to store file
        target_path = f'pipeline/{pk_pipeline}/{str(timezone.now().replace(tzinfo=None))}/{file}'
        saved_location = storage.save(target_path, file)

        # Connect uploaded file to pipeline using intermediary model
        pipeline_file = PipelineFile.objects.create(pipeline=pipeline, file=file, path=saved_location)

        # Check if pipeline is stale
        past_due = is_stable(pk_pipeline)
        data = {
            'pipeline_id': pk_pipeline,
            'upload_date': pipeline_file.upload_date,
            'past_due': past_due,
            'filename': str(file),
            'file': saved_location,
            'template': pipeline_file.template_file
        }

        return Response(status=status.HTTP_200_OK, data=data)

class PipelineTemplateFileUploadAPIView(generics.CreateAPIView):
    """Upload files to an approved pipeline"""
    queryset = Pipeline
    serializer_class = serializers.FileUploadSerializer

    def create(self, request):
        # Get the uploaded file from the request
        file = request.FILES.get('file')

        return Response(status=status.HTTP_200_OK, data={"constraints": generate_types(file)})

class PipelineFileListAPIView(generics.ListAPIView):
    """View uploaded files for a specific pipeline"""
    serializer_class = serializers.PipelineFileSerializer
    queryset = PipelineFile.objects.all()

    def get(self, request, pk_pipeline):
        # Check to see if a user is allowed to view this pipeline
        check_user_permissions(request, pk_pipeline, Uploader)

        # Check to make sure pipeline exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404
        instance = PipelineFile.objects.filter(pipeline=pipeline)

        return Response(serializers.PipelineFileSerializer(instance, many=True).data)

class PipelineFileRetrieveAPIView(generics.RetrieveAPIView):
    """View uploaded file for a specific pipeline"""
    serializer_class = serializers.PipelineFileSerializer
    queryset = PipelineFile.objects.all()

    def get(self, request, pk_pipeline, pk_pipelinefile):
        # Check to see if a user is allowed to view this pipeline
        check_user_permissions(request, pk_pipeline, Uploader)

        # Check to make sure pipeline exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404
        instance = PipelineFile.objects.filter(pipeline=pipeline)

        # Get the specific uploaded file from the pipeline
        try:
            uploaded_file = instance.get(pk=pk_pipelinefile)
        except PipelineFile.DoesNotExist:
            raise Http404

        return Response(serializers.PipelineFileSerializer(uploaded_file).data)

class ValidateFileAPIView(generics.ListAPIView):
    serializer_class = PipelineFile
    queryset = PipelineFile.objects.all()

    def get(self, request, pk_pipeline, pk_pipelinefile):
        # Verify pipeline and pipeline file exist
        try:
            Pipeline.objects.get(pk=pk_pipeline)
            pipeline_file = PipelineFile.objects.get(pk=pk_pipelinefile)
        except (Pipeline.DoesNotExist, PipelineFile.DoesNotExist):
            raise Http404

        return Response(data={"errors": validate(pipeline_file=pipeline_file)})

class PipelineDeadlineAPIView(generics.ListAPIView):
    """Get the remaining time for a pipeline to be stable"""
    serializer_class = Pipeline
    queryset = Pipeline.objects.all()

    def get(self, request, pk_pipeline):
        # Verify pipeline and pipeline file exist
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404

        return Response(status=status.HTTP_200_OK, data={'deadline': get_deadline(pipeline.pk)})

class PipelineNotificationListAPIView(generics.ListAPIView):
    serializer_class = PipelineNotification
    queryset = Pipeline.objects.all()

    def get(self, request, pk_pipeline):
        # Verify pipeline and pipeline file exist
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except Pipeline.DoesNotExist:
            raise Http404

        instance = PipelineNotification.objects.filter(pipeline=pipeline)

        return Response(serializers.PipelineNotificationSerializer(instance=instance, many=True).data)
