from django.core.exceptions import PermissionDenied


def is_user_allowed(request, pk, model):
    # Get current user instance
    user = request.user

    # Get managers for the current pipeline
    group = model.objects.filter(pipeline_id=pk).values_list('user', flat=True)

    # Staff users can perform any operation
    if not (user.is_staff or user.id in group):
        return False
    return True

def check_user_permissions(request, pk, model):
    if not is_user_allowed(request, pk, model):
        raise PermissionDenied
