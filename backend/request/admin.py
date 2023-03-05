from django.contrib import admin

from .models import Request

class RequestHistoryAdmin(admin.ModelAdmin):
    list_display = [
        'title',
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

admin.site.register(Request, RequestHistoryAdmin)
