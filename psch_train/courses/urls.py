from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('<int:course_id>/start-quiz/', views.start_quiz, name='start_quiz'),
    path('quiz/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:attempt_id>/result/', views.quiz_result, name='quiz_result'),
]
