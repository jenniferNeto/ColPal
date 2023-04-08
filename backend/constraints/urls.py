from django.urls import path

from . import views

# Include / at the end of endpoints or unexpected errors will be raised
urlpatterns = [
    path('<int:pk_pipeline>/files/<int:pk_pipelinefile>/constraints/', views.ConstraintsListAPIView.as_view()),
]
