from django.contrib import admin
from .models import Viewer, Uploader, Manager

# Register your models here.
admin.site.register(Viewer)
admin.site.register(Uploader)
admin.site.register(Manager)
