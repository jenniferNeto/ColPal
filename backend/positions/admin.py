from django.contrib import admin
from .models import Viewer, Uploader, Manager

class PositionAdminModel(admin.ModelAdmin):
    list_display = [
        'user',
        'pipeline',
    ]

# Register all postions on the admin site
admin.site.register(Viewer, PositionAdminModel)
admin.site.register(Uploader, PositionAdminModel)
admin.site.register(Manager, PositionAdminModel)
