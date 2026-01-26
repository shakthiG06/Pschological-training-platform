from django.urls import path
from .views import evaluate_session

urlpatterns = [
    path('<int:session_id>/', evaluate_session, name='evaluate'),
]
