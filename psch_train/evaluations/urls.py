from django.urls import path
from .views import evaluate_session, evaluation_result

urlpatterns = [
    path("<int:session_id>/", evaluate_session, name="evaluate"),
    path("result/<int:session_id>/", evaluation_result, name="evaluation_result"),
]
