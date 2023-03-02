from django.urls import path

from . import views


urlpatterns = [
    path("<int:pk_pipeline>/viewers/", views.ViewerListAPIView.as_view()),
    path("<int:pk_pipeline>/uploaders/", views.UploaderListAPIView.as_view()),
    path("<int:pk_pipeline>/managers/", views.ManagerListAPIView.as_view())

]
