from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from chat.models import ChatSession
from evaluations.models import Evaluation

# =========================
# ROLE SELECT
# =========================
def role_select(request):
    return render(request, "role_select.html")


# =========================
# LOGIN
# =========================
def login_view(request, role):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.profile.role != role:
                messages.error(request, "You are not authorized for this role.")
                return redirect(request.path)

            login(request, user)

            if role == "student":
                return redirect("student_dashboard")
            else:
                return redirect("staff_dashboard")

        messages.error(request, "Invalid credentials")

    return render(request, "login.html", {"role": role})


# =========================
# LOGOUT  ✅ (IMPORTANT)
# =========================
def logout_view(request):
    logout(request)
    return redirect("role_select")


# =========================
# STUDENT DASHBOARD
# =========================
@login_required
def student_dashboard(request):
    latest_session = (
        ChatSession.objects
        .filter(student=request.user)
        .order_by("-created_at")
        .first()
    )

    evaluation = None
    if latest_session:
        evaluation = Evaluation.objects.filter(session=latest_session).first()

    return render(
        request,
        "student_dashboard.html",
        {
            "latest_session": latest_session,
            "evaluation": evaluation
        }
    )


# =========================
# STAFF DASHBOARD
# =========================
@login_required
def staff_dashboard(request):
    if request.user.profile.role != "staff":
        return render(request, "unauthorized.html")

    pending_sessions = ChatSession.objects.filter(
        evaluation__isnull=True
    ).select_related("student", "patient")

    evaluated_sessions = ChatSession.objects.filter(
        evaluation__isnull=False
    ).select_related("student", "patient")

    return render(
        request,
        "staff_dashboard.html",
        {
            "pending_sessions": pending_sessions,
            "evaluated_sessions": evaluated_sessions
        }
    )
