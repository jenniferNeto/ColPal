from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pipelines/', include('pipeline.urls')),
    path('pipelines/', include('positions.urls')),
    path('users/', include('authentication.urls')),
    path('', home_view),
]