from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.http import Http404

from simple_history.utils import update_change_reason

from authentication.utils import check_user_permissions
from positions.models import Viewer, Uploader, Manager
from pipeline.models import Pipeline

from .models import Request
from .serializers import RequestSerializer, RequestUpdateSerializer


class RequestListAPIView(generics.ListAPIView):
    """View requests for every pipeline"""
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    # Users must be admins to view requests on all pipelines
    permission_classes = [IsAdminUser]

class RequestPipelineListAPIView(generics.RetrieveAPIView):
    """View requests for a specific pipeline"""
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    def get(self, request, pk_pipeline):
        # Only managers can view requests for a pipeline
        check_user_permissions(request, pk_pipeline, Manager)
        instance = Request.objects.filter(pipeline_id=pk_pipeline)
        return Response(RequestSerializer(instance, many=True).data)

class RequestUpdateDetailAPIView(generics.UpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestUpdateSerializer

    def put(self, request, *args, **kwargs):
        request_id = self.kwargs['pk_request']
        instance = Request.objects.filter(pk=request_id).first()

        # If either instance is none updating is meaningless
        if instance is None or instance.pipeline is None:
            raise Http404

        # Only managers can accept request changes
        check_user_permissions(request, instance.pipeline_id, Manager)

        # If the request is already accepted don't reaccept the changes
        # TODO: I don't think this is working
        if instance.accept_changes == request.data['accept_changes'] and instance.accept_changes == '1':
            return Response(status.HTTP_208_ALREADY_REPORTED)

        # Update the Request model
        instance.accept_changes = request.data['accept_changes']
        instance.response = request.data['response']
        instance.save()

        # Check if request is accepted
        if instance.accept_changes == '1':
            # Update pipeline with requested changes
            self.update_instance(instance=instance.pipeline,
                                 title=instance.title,
                                 upload_frequency=instance.upload_frequency,
                                 is_active=instance.is_active,
                                 update_reason=instance.update_reason)
        return Response(status.HTTP_200_OK)

    def get(self, request, pk_request):
        # Get the requested model
        instance = Request.objects.filter(pk=pk_request).first()

        # Check model's existance
        if instance is None:
            raise Http404

        # Only managers can view requested changes
        check_user_permissions(request, instance.pipeline_id, Manager)
        return Response(RequestSerializer(instance).data)

    def update_instance(self, instance: Pipeline, **kwargs):
        # Data should have three optinal update fields
        # request_title, request_upload_frequency, request_is_active
        print(kwargs)

        # Attempting to fix the history_change_reason failure
        n_instance = Pipeline.objects.filter(pk=instance.pk).first()

        if not n_instance:
            return
        
        print(type(n_instance))
        print(n_instance.history)

        print(instance)

        n_instance.title = kwargs['title']
        n_instance.upload_frequency = kwargs['upload_frequency']
        n_instance.is_active = kwargs['is_active']

        update_change_reason(n_instance, kwargs['update_reason'])

        # Save changes on the instance
        # This will also generate a historical model of the changes
        n_instance.save()
"""

TODO: Requests need their own endpoints so that anyone who is a Manager of a specific pipeline, or superuser,
can look at all the requests made for a pipeline. The endpoint will allow the user to approve or reject any of
the modifications.

"""
