from django.urls import path
from .views import (
    role_select,
    login_view,
    student_dashboard,
    staff_dashboard,
    staff_assign_students,
    about_us,
)

urlpatterns = [
    path("", role_select, name="role_select"),
    path("login/<str:role>/", login_view, name="login"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
    path("staff/dashboard/", staff_dashboard, name="staff_dashboard"),
    path("staff/assign-students/", staff_assign_students, name="staff_assign_students"),
    path("about/", about_us, name="about_us"),
]
