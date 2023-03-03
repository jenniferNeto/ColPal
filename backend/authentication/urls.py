from django.urls import path
from . import views

# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('', views.UsersListAPIView.as_view(), name="Get Users"),
    path('<int:pk>/', views.UsersDetailAPIView.as_view(), name="Get Users"),
    path('login/', views.UserLoginAPIView.as_view()),
    path('logout/', views.UserLogoutAPIView.as_view())
]
