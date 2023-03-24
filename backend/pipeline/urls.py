from django.urls import path, include

from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'', views.FileUploadViewSet, basename='file-upload')

# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('', views.PipelineListAPIView.as_view()),
    path('approved/', views.ApprovedPipelineListAPIView.as_view()),
    path('create/', views.PipelineCreateAPIView.as_view()),
    path('<int:pk_pipeline>/', views.PipelineDetailAPIView.as_view()),
    path('<int:pk_pipeline>/update/', views.PipelineUpdateAPIView.as_view()),
    path('<int:pk_pipeline>/history/', views.PipelineHistoricalRecordsRetrieveAPIView.as_view()),
    path('user/<int:pk>/', views.UserPipelinesListAPIView.as_view()),
    path('<int:pk_pipeline>/upload/', include(router.urls))
]
