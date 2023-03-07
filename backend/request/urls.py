from django.urls import path

from . import views

urlpatterns = [
    path('requests/', views.RequestListAPIView.as_view()),
    path('<int:pk_pipeline>/requests/', views.RequestPipelineListAPIView.as_view()),
    path('requests/<int:pk_request>/', views.RequestUpdateDetailAPIView.as_view()),
]
