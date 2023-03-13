from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.contrib.auth.models import User

from positions.models import PipelineUser

def is_user_allowed(request, pk, model):
    # Get current user instance
    user: User = request.user

    # Get positions for the current pipeline
    positions: QuerySet[PipelineUser] = model.objects.filter(pipeline_id=pk)

    # Get user object for each found position
    user_positions = [obj.user.pk if obj.user is not None else None for obj in positions]

    # If user is not a super user and is not found in user_positions return false
    if not (user.is_superuser or user.pk in user_positions):
        return False
    return True

def check_user_permissions(request, pk, model):
    if not is_user_allowed(request, pk, model):
        raise PermissionDenied
