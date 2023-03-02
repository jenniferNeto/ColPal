from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Pipeline

class PipelineHistoryAdmin(SimpleHistoryAdmin):
    list_display = [
        'id',
        'title',
        'upload_frequency',
        'is_approved',
        'is_active',
        'approved_date'
    ]
    history_list_display = ['status']
    search_fields = [
        'id',
        'title',
        'upload_frequency',
        'is_approved',
        'is_active',
        'approved_date'
    ]

admin.site.register(Pipeline, PipelineHistoryAdmin)
