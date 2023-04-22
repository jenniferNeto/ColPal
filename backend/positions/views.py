from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.http import Http404

from pipeline.models import Pipeline
from authentication.utils import check_user_permissions

from .models import Viewer, Uploader, Manager
from .utils import position_email
from . import serializers

User = get_user_model()


class IsViewerRequired(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        check_user_permissions(request, kwargs['pk_pipeline'], Viewer)
        return super().get(request, *args, **kwargs)

class ViewerListAPIView(IsViewerRequired):
    """View all Viewers for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Viewer.objects.filter(pipeline_id=pipeline_id)

    serializer_class = serializers.ViewerSerializer

class UploaderListAPIView(IsViewerRequired):
    """View all Uploaders for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Uploader.objects.filter(pipeline_id=pipeline_id)

    serializer_class = serializers.UploaderSerializer

class ManagerListAPIView(IsViewerRequired):
    """View all Managers for a specific pipeline"""
    def get_queryset(self):
        pipeline_id = self.kwargs['pk_pipeline']
        return Manager.objects.filter(pipeline_id=pipeline_id)

    serializer_class = serializers.ManagerSerializer

class ViewerCreateAPIView(generics.CreateAPIView):
    """Create a new viewer for a specific pipeline"""
    queryset = Viewer.objects.none()
    serializer_class = serializers.ViewerPositionSerializer

    def post(self, request, pk_pipeline):
        # Check user is a manager
        check_user_permissions(request, pk_pipeline, Manager)

        try:
            user = User.objects.get(pk=request.data['id'])
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except (User.DoesNotExist, Pipeline.DoesNotExist):
            raise Http404

        # Attempt to create a Viewer on the pipeline which requires a unique instance
        try:
            Viewer.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            raise ValidationError(detail={"detail": "User is already a viewer"})

        position_email("You have a new position!", pk_pipeline, "position_added.html",
                       user, context={"username": user, "position": "Viewer", "title": pipeline})
        return Response(request.data)

class UploaderCreateAPIView(generics.CreateAPIView):
    """Create a new viewer for a specific pipeline"""
    queryset = Uploader.objects.none()
    serializer_class = serializers.UploaderPositionSerializer

    def post(self, request, pk_pipeline):
        # Check user is a manager
        check_user_permissions(request, pk_pipeline, Manager)

        try:
            user = User.objects.get(pk=request.data['id'])
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except (User.DoesNotExist, Pipeline.DoesNotExist):
            raise Http404

        # Attempt to create an Uploader on the pipeline which requires a unique instance
        try:
            Uploader.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            raise ValidationError(detail={"detail": "User is already an uploader"})

        # Attempt to add user as an uploader and viewer as well
        try:
            Viewer.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            pass

        position_email("You have a new position!", pk_pipeline, "position_added.html",
                       user, context={"username": user, "position": "Uploader", "title": pipeline})
        return Response(request.data)

class ManagerCreateAPIView(generics.CreateAPIView):
    """Create a new viewer for a specific pipeline"""
    queryset = Uploader.objects.none()
    serializer_class = serializers.ManagerPositionSerializer

    def post(self, request, pk_pipeline):
        # Check user is a manager
        check_user_permissions(request, pk_pipeline, Manager)

        try:
            user = User.objects.get(pk=request.data['id'])
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
        except (User.DoesNotExist, Pipeline.DoesNotExist):
            raise Http404

        # Attempt to create a Manager on the pipeline which requires a unique instance
        try:
            Manager.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            raise ValidationError(detail={"detail": "User is already a manager"})

        # Attempt to add user as an uploader and viewer as well
        try:
            Viewer.objects.create(user=user, pipeline=pipeline)
            Uploader.objects.create(user=user, pipeline=pipeline)
        except IntegrityError:
            pass

        position_email("You have a new position!", pk_pipeline, "position_added.html",
                       user, context={"username": user, "position": "Manager", "title": pipeline})
        return Response(request.data)

class ViewerDeleteAPIView(generics.UpdateAPIView):
    """Delete a viewer from a pipeline"""
    # Deleting as a viewer deletes all other roles
    queryset = Viewer.objects.none()
    serializer_class = serializers.ViewerPositionSerializer

    def put(self, request, pk_pipeline):
        # Validate pipeline and user exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
            user = User.objects.get(pk=request.data['id'])
        except (Pipeline.DoesNotExist, User.DoesNotExist):
            raise Http404
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Validate user is a viewer
        try:
            viewer = Viewer.objects.get(pipeline=pipeline, user=user)
        except Viewer.DoesNotExist:
            return Response(status=status.HTTP_409_CONFLICT, data={"detail": "User is not a viewer"})

        # If viewer exists, check for uploader and manager roles
        uploader = Uploader.objects.filter(pipeline=pipeline, user=user)
        manager = Manager.objects.filter(pipeline=pipeline, user=user)

        # If the user is a manager, check to see if its the last manager
        if manager:
            if Manager.objects.count() == 1:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"detail": "Cannot delete last manager"})
            else:
                manager[0].delete()
        if uploader:
            uploader[0].delete()

        viewer.delete()
        position_email("You have been removed!", pk_pipeline, "position_removed.html",
                       user, context={"username": user, "position": "Viewer", "title": pipeline})
        return Response(status=status.HTTP_200_OK)

class UploaderDeleteAPIView(generics.UpdateAPIView):
    """Delete a viewer from a pipeline"""
    # Deleting as a viewer deletes all other roles
    queryset = Uploader.objects.none()
    serializer_class = serializers.UploaderPositionSerializer

    def put(self, request, pk_pipeline):
        # Validate pipeline and user exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
            user = User.objects.get(pk=request.data['id'])
        except (Pipeline.DoesNotExist, User.DoesNotExist):
            raise Http404
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Validate user is an uploader
        try:
            uploader = Uploader.objects.get(pipeline=pipeline, user=user)
        except Uploader.DoesNotExist:
            return Response(status=status.HTTP_409_CONFLICT, data={"detail": "User is not an uploader"})

        uploader.delete()
        position_email("You have been removed!", pk_pipeline, "position_removed.html",
                       user, context={"username": user, "position": "Uploader", "title": pipeline})
        return Response(status=status.HTTP_200_OK)

class ManagerDeleteAPIView(generics.UpdateAPIView):
    """Delete a viewer from a pipeline"""
    # Deleting as a viewer deletes all other roles
    queryset = Manager.objects.none()
    serializer_class = serializers.ManagerPositionSerializer

    def put(self, request, pk_pipeline):
        # Validate pipeline and user exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
            user = User.objects.get(pk=request.data['id'])
        except (Pipeline.DoesNotExist, User.DoesNotExist):
            raise Http404
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Validate user is a manager
        try:
            manager = Manager.objects.get(pipeline=pipeline, user=user)
        except Manager.DoesNotExist:
            return Response(status=status.HTTP_409_CONFLICT, data={"detail": "User is not a manager"})

        if len(Manager.objects.filter(pipeline=pipeline)) == 1:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"detail": "Cannot delete last manager"})
        manager.delete()
        position_email("You have been removed!", pk_pipeline, "position_removed.html",
                       user, context={"username": user, "position": "Manager", "title": pipeline})
        return Response(status=status.HTTP_200_OK)

class UserDeleteAPIView(generics.UpdateAPIView):
    """Delete a user from a pipeline"""
    # Deleting as a user deletes all roles
    queryset = Viewer.objects.none()
    serializer_class = serializers.ViewerPositionSerializer

    def put(self, request, pk_pipeline):
        # Validate pipeline and user exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
            user = User.objects.get(pk=request.data['id'])
        except (Pipeline.DoesNotExist, User.DoesNotExist):
            raise Http404
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Find all user positions
        viewer = Viewer.objects.filter(pipeline=pipeline, user=user)
        uploader = Uploader.objects.filter(pipeline=pipeline, user=user)
        manager = Manager.objects.filter(pipeline=pipeline, user=user)

        # If the user is a manager, check to see if its the last manager
        if manager:
            if Manager.objects.count() == 1:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data={"detail": "Cannot delete last manager"})
            else:
                manager[0].delete()
        if uploader:
            uploader[0].delete()
        if viewer:
            viewer[0].delete()
        position_email("You have been removed!", pk_pipeline, "position_removed.html",
                       user, context={"username": user, "position": "all", "title": pipeline})
        return Response(status=status.HTTP_200_OK)

class RolesListAPIView(generics.ListAPIView):
    """Delete a user from a pipeline"""
    # Deleting as a user deletes all roles
    queryset = Viewer.objects.none()
    serializer_class = serializers.ViewerPositionSerializer

    def get(self, request, pk_pipeline):
        # Validate pipeline and user exists
        try:
            pipeline = Pipeline.objects.get(pk=pk_pipeline)
            user = User.objects.get(username=request.user)
        except Pipeline.DoesNotExist:
            raise Http404

        viewer = Viewer.objects.filter(pipeline=pipeline, user=user)
        uploader = Uploader.objects.filter(pipeline=pipeline, user=user)
        manager = Manager.objects.filter(pipeline=pipeline, user=user)

        data = {}
        if viewer:
            data['viewer'] = serializers.ViewerSerializer(viewer[0]).data
        if uploader:
            data['uploader'] = serializers.PipelineUserSerializer(uploader[0]).data
        if manager:
            data['manager'] = serializers.PipelineUserSerializer(manager[0]).data
        return Response(status=status.HTTP_200_OK, data=data)
