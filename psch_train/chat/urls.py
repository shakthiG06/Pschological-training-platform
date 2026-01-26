from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),          # /chat/
    path('<int:patient_id>/', views.chat_view, name='chat'),  # /chat/1/
]
