from django.urls import path

from . import views

# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('', views.PipelineListAPIView.as_view()),
    path('approved/', views.ApprovedPipelineListAPIView.as_view()),
    path('create/', views.PipelineCreateAPIView.as_view()),
    path('<int:pk_pipeline>/', views.PipelineDetailAPIView.as_view()),
    path('<int:pk_pipeline>/update/', views.PipelineUpdateAPIView.as_view()),
    path('<int:pk_pipeline>/history/', views.PipelineHistoricalRecordsRetrieveAPIView.as_view()),
    path('<int:pk_pipeline>/upload/', views.PipelineFileUpload.as_view()),
    path('<int:pk_pipeline>/status/', views.PipelineStatusAPIView.as_view()),
    path('user/<int:pk>/', views.UserPipelinesListAPIView.as_view()),
]
