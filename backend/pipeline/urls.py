from django.urls import path

from . import views


urlpatterns = [
    path("", views.PipelineListAPIView.as_view()),
    path("approved", views.ApprovedPipelineListAPIView.as_view()),
    path("create", views.PipelineCreateAPIView.as_view()),
    path("<int:pk>", views.PipelineDetailAPIView.as_view()),
    path("<int:pk>/update", views.PipelineUpdateAPIView.as_view()),
    path("<int:pk_pipeline>/history", views.PipelineHistoricalRecordsRetrieveAPIView.as_view()),
]
