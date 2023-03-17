from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('', views.UsersListAPIView.as_view(), name="Get Users"),
    path('<int:pk>/', views.UsersDetailAPIView.as_view(), name="Get Users"),
    path('login/', views.UserLoginAPIView.as_view()),
    path('logout/', views.UserLogoutAPIView.as_view()),

    path('obtain/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
