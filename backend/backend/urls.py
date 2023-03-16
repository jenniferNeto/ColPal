from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('authentication.urls')),
    path('pipelines/', include('pipeline.urls')),
    path('pipelines/', include('positions.urls')),
    path('pipelines/', include('request.urls')),
]
