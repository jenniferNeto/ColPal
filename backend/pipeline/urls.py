from django.urls import path
from . import views

urlpatterns = [
    path("", views.PipelineListCreateAPIView.as_view()),
    path("<int:pk>", views.PipelineDetailAPIView.as_view()),
]
