from django.contrib import admin
from django.urls import path, include
from .views import home_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('authentication.urls')),
    path('pipelines/', include('pipeline.urls')),
    path('pipelines/', include('positions.urls')),  # causing auth table error
    path('pipelines/', include('request.urls')),
    path('', home_view),
]
