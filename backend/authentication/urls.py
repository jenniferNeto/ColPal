from django.urls import path
from . import views

urlpatterns = [
    path('', views.UsersListAPIView.as_view(), name="Get Users"),
    path('<int:pk>', views.UsersDetailAPIView.as_view(), name="Get Users")
]
