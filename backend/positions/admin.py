from django.contrib import admin
from .models import Viewer, Uploader, Manager

class PositionAdminModel(admin.ModelAdmin):
    list_display = [
        'user',
        'pipeline',
    ]

# Register your models here.
admin.site.register(Viewer, PositionAdminModel)
admin.site.register(Uploader, PositionAdminModel)
admin.site.register(Manager, PositionAdminModel)
