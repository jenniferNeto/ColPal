from django.urls import path

from .views import RequestListAPIView, RequestDetailAPIView

urlpatterns = [
    path('requests/', RequestListAPIView.as_view()),
    path('<int:pk_pipeline>/requests/', RequestDetailAPIView.as_view()),
]
