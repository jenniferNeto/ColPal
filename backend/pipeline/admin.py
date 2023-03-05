from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Pipeline

class PipelineHistoryAdmin(SimpleHistoryAdmin):
    list_display = [
        'title',
        'upload_frequency',
        'is_approved',
        'is_active',
        'approved_date'
    ]
    history_list_display = ['status']
    search_fields = [
        'title',
        'upload_frequency',
        'is_approved',
        'is_active',
        'approved_date'
    ]

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Pipeline, PipelineHistoryAdmin)
