from django.urls import path

from . import views


# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('<int:pk_pipeline>/positions/viewers/', views.ViewerListAPIView.as_view()),
    path('<int:pk_pipeline>/positions/viewers/add/', views.ViewerCreateAPIView.as_view()),
    path('<int:pk_pipeline>/positions/viewers/delete/', views.ViewerDeleteAPIView.as_view()),
    path('<int:pk_pipeline>/positions/uploaders/', views.UploaderListAPIView.as_view()),
    path('<int:pk_pipeline>/positions/uploaders/add/', views.UploaderCreateAPIView.as_view()),
    path('<int:pk_pipeline>/positions/uploaders/delete/', views.UploaderDeleteAPIView.as_view()),
    path('<int:pk_pipeline>/positions/managers/', views.ManagerListAPIView.as_view()),
    path('<int:pk_pipeline>/positions/managers/add/', views.ManagerCreateAPIView.as_view()),
    path('<int:pk_pipeline>/positions/managers/delete/', views.ManagerDeleteAPIView.as_view()),
    path('<int:pk_pipeline>/positions/delete/', views.UserDeleteAPIView.as_view()),

]
