from django.core.exceptions import PermissionDenied


def check_user_permissions(request, pk, model):
    # Get current user instance
    user = request.user

    # Get managers for the current pipeline
    group = model.objects.filter(pipeline_id=pk).values_list('user', flat=True)
    print('Group:', group)

    # Staff users can perform any operation
    if not user.is_staff and user.id not in group:
        raise PermissionDenied
