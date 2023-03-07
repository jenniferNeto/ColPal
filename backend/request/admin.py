from django.contrib import admin

from .models import Request

class RequestAdminModel(admin.ModelAdmin):
    list_display = [
        'title',
        'id',
        'upload_frequency',
        'update_reason',
        'accept_changes'
    ]

    readonly_fields = [
        'pipeline',
        'update_reason',
        'last_modified',
        'approved_date',
    ]

# Add request to admin site
admin.site.register(Request, RequestAdminModel)
