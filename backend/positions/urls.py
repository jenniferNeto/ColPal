from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk_pipeline>/viewers/", views.ViewerRetrieveAPIView.as_view()),
    path("<int:pk_pipeline>/uploaders/", views.UploaderRetrieveAPIView.as_view()),
    path("<int:pk_pipeline>/managers/", views.ManagerRetrieveAPIView.as_view())

]
