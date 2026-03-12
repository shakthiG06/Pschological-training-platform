"""
URL configuration for psch_train project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# ✅ IMPORT VIEWS EXPLICITLY
from frontend.views import (
    role_select,
    login_view,
    logout_view,
    student_dashboard,
    staff_dashboard,
    about_us,
    student_profile,
    hide_help,
    staff_assessments,
    create_assessment,
    publish_assessment,
    delete_assessment,
    view_submissions,
    staff_students,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Role selection & auth
    path("", role_select, name="role_select"),
    path("login/<str:role>/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Dashboards (with shortcuts)
    path("student/", lambda r: redirect("student_dashboard")),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
    path("student/profile/", student_profile, name="student_profile"),
    path("staff/", lambda r: redirect("staff_dashboard")),
    path("staff/dashboard/", staff_dashboard, name="staff_dashboard"),
    path("staff/assessments/", staff_assessments, name="staff_assessments"),
    path("staff/assessments/create/", create_assessment, name="create_assessment"),
    path("staff/assessments/<int:pk>/publish/", publish_assessment, name="publish_assessment"),
    path("staff/assessments/<int:pk>/delete/", delete_assessment, name="delete_assessment"),
    path("staff/assessments/<int:pk>/submissions/", view_submissions, name="view_submissions"),
    path("staff/students/", staff_students, name="staff_students"),

    # API endpoints
    path("api/hide-help/", hide_help, name="hide_help"),

    # About Us
    path("about/", about_us, name="about_us"),

    # Other apps
    path("chat/", include("chat.urls")),
    path("courses/", include("courses.urls")),
    path("evaluate/", include("evaluations.urls")),
]
