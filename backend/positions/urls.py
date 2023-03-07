from django.urls import path

from . import views


# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('<int:pk_pipeline>/viewers/', views.ViewerListAPIView.as_view()),
    path('<int:pk_pipeline>/viewers/add/', views.ViewerCreateAPIView.as_view()),

    path('<int:pk_pipeline>/uploaders/', views.UploaderListAPIView.as_view()),
    path('<int:pk_pipeline>/uploaders/add/', views.UploaderCreateAPIView.as_view()),

    path('<int:pk_pipeline>/managers/', views.ManagerListAPIView.as_view()),
    path('<int:pk_pipeline>/managers/add/', views.ManagerCreateAPIView.as_view()),

]
