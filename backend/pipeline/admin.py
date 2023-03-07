from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Pipeline

class PipelineHistoryAdmin(SimpleHistoryAdmin):
    """View endpoint for Pipelines in the admin site"""
    list_display = [
        'title',
        'id',
        'upload_frequency',
        'is_approved',
        'is_active',
        'approved_date'
    ]
    history_list_display = ['status']
    search_fields = [
        'title',
        'id',
        'upload_frequency',
        'is_approved',
        'is_active',
        'approved_date'
    ]

    def has_change_permission(self, request, obj=None):
        return False

# Register the model in the admin site
admin.site.register(Pipeline, PipelineHistoryAdmin)
