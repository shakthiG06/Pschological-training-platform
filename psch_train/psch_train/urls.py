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

# ✅ IMPORT VIEWS EXPLICITLY
from frontend.views import (
    role_select,
    login_view,
    logout_view,
    student_dashboard,
    staff_dashboard,
    about_us,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Role selection & auth
    path("", role_select, name="role_select"),
    path("login/<str:role>/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Dashboards
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
    path("staff/dashboard/", staff_dashboard, name="staff_dashboard"),

    # About Us
    path("about/", about_us, name="about_us"),

    # Other apps
    path("chat/", include("chat.urls")),
    path("courses/", include("courses.urls")),
    path("evaluate/", include("evaluations.urls")),
]
