from django.urls import path

from . import views

# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('<int:pk_pipeline>/constraints/', views.ConstraintsListAPIView.as_view()),
    path('<int:pk_pipeline>/constraints/<int:pk_constraint>/', views.ConstraintUpdateAPIView.as_view()),
]
