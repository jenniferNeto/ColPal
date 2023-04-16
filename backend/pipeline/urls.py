from django.urls import path

from . import views
from .utils import cron_is_stable

from apscheduler.schedulers.background import BackgroundScheduler

import os

# Code is being run here since urls.py gets loaded a single time by the application
# Need to ignore scheduler to run django tests during github workflow

# To run django test cases this has to be disabled. Pipelines will not be automatically checked for stability
if os.environ.get('IGNORE_SCHEDULER') is None or os.environ.get('IGNORE_SCHEDULER') == 'false':
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(cron_is_stable, 'interval', seconds=5)

# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('', views.PipelineListAPIView.as_view()),
    path('approved/', views.ApprovedPipelineListAPIView.as_view()),
    path('create/', views.PipelineCreateAPIView.as_view()),
    path('<int:pk_pipeline>/', views.PipelineDetailAPIView.as_view()),
    path('<int:pk_pipeline>/update/', views.PipelineUpdateAPIView.as_view()),
    path('<int:pk_pipeline>/history/', views.PipelineHistoricalRecordsRetrieveAPIView.as_view()),
    path('<int:pk_pipeline>/upload/', views.PipelineFileUploadAPIView.as_view()),
    path('upload/template/', views.PipelineTemplateFileUploadAPIView.as_view()),
    path('<int:pk_pipeline>/status/', views.PipelineStatusAPIView.as_view()),
    path('<int:pk_pipeline>/files/', views.PipelineFileListAPIView.as_view()),
    path('<int:pk_pipeline>/files/<int:pk_pipelinefile>/', views.PipelineFileRetrieveAPIView.as_view()),
    path('<int:pk_pipeline>/files/<int:pk_pipelinefile>/validate/', views.ValidateFileAPIView.as_view()),
    path('<int:pk_pipeline>/deadline/', views.PipelineDeadlineAPIView.as_view()),
    path('<int:pk_pipeline>/notifications/', views.PipelineNotificationListAPIView.as_view()),
    path('user/<int:pk>/', views.UserPipelinesListAPIView.as_view()),
]
