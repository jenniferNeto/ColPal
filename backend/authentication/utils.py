from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from positions.models import PipelineUser
from pipeline.models import Pipeline

def is_user_allowed(request, pk, model):
    # Get current user instance
    user: User = request.user

    print("Request:", request)
    print("Primary Key:", pk)
    print("Model:", model)
    print("User:", user)

    # Get managers for the current pipeline
    position: PipelineUser = model.objects.filter(pipeline_id=pk)
    position2 = model.objects.filter(pipeline_id=pk)
    p = model.objects.all()

    print("Position:", position)
    print("Position 2:", position2)
    print("Unfiltered:", p)

    print()
    print("All pipelines:")
    [print("Pipeline ID:", e.pk) for e in Pipeline.objects.all()]
    print("======================================================")

    a = p[0] if p.count() > 0 else None
    if a is not None:
        print("Pipeline ID:", a.pipeline_id)
    print()

    # Staff users can perform any operation
    # print("======================================================")
    # print(user.pk)
    # print(position)
    # print(user.pk in position)
    # print("======================================================")
    if not (user.is_superuser or user.pk in position):
        return False
    return True

def check_user_permissions(request, pk, model):
    if not is_user_allowed(request, pk, model):
        raise PermissionDenied
