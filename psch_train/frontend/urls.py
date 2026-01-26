from django.urls import path
from .views import (
    role_select,
    login_view,
    student_dashboard,
    staff_dashboard,
)

urlpatterns = [
    path("", role_select, name="role_select"),
    path("login/<str:role>/", login_view, name="login"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
    path("staff/dashboard/", staff_dashboard, name="staff_dashboard"),
]
