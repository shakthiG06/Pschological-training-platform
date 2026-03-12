from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count
from collections import defaultdict
from datetime import timedelta
from chat.models import ChatSession
from evaluations.models import Evaluation
from courses.models import Course, Assessment, Enrollment


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
# ABOUT US
# =========================
def about_us(request):
    return render(request, "about_us.html")


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
# STUDENT PROFILE
# =========================
@login_required
def student_profile(request):
    profile = request.user.profile
    
    if request.method == "POST":
        # Update profile fields
        full_name = request.POST.get("full_name", "").strip()
        if full_name:
            name_parts = full_name.split(" ", 1)
            request.user.first_name = name_parts[0]
            request.user.last_name = name_parts[1] if len(name_parts) > 1 else ""
            request.user.save()
        
        profile.phone = request.POST.get("phone", "").strip() or None
        profile.institution = request.POST.get("institution", "").strip() or None
        profile.student_class = request.POST.get("student_class", "").strip() or None
        profile.place = request.POST.get("place", "").strip() or None
        profile.bio = request.POST.get("bio", "").strip() or None
        profile.avatar_color = request.POST.get("avatar_color", "rose")
        
        dob = request.POST.get("date_of_birth", "").strip()
        if dob:
            try:
                from datetime import datetime
                profile.date_of_birth = datetime.strptime(dob, "%Y-%m-%d").date()
            except ValueError:
                pass
        
        # Check if profile is complete
        profile.is_profile_complete = all([
            profile.institution,
            profile.student_class,
            profile.place
        ])
        
        profile.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("student_profile")
    
    avatar_colors = ['rose', 'blue', 'emerald', 'purple', 'amber', 'cyan', 'pink', 'indigo']
    
    return render(request, "student_profile.html", {
        "profile": profile,
        "avatar_colors": avatar_colors,
        "completion_percentage": profile.get_completion_percentage()
    })


# =========================
# HIDE HELP DASHBOARD API
# =========================
@login_required
@require_POST
def hide_help(request):
    request.user.profile.show_help = False
    request.user.profile.save()
    return JsonResponse({"status": "ok"})


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


# =========================
# STAFF ASSESSMENTS
# =========================
@login_required
def staff_assessments(request):
    if request.user.profile.role != "staff":
        return render(request, "unauthorized.html")
    
    courses = Course.objects.prefetch_related('assessments').all()
    assessments = Assessment.objects.all()
    
    return render(request, "staff_assessments.html", {
        "courses": courses,
        "total_assessments": assessments.count(),
        "published_count": assessments.filter(status='published').count(),
        "draft_count": assessments.filter(status='draft').count(),
    })


# =========================
# CREATE ASSESSMENT
# =========================
@login_required
@require_POST
def create_assessment(request):
    if request.user.profile.role != "staff":
        return render(request, "unauthorized.html")
    
    course_id = request.POST.get("course")
    course = get_object_or_404(Course, id=course_id)
    
    assessment = Assessment.objects.create(
        course=course,
        title=request.POST.get("title", ""),
        description=request.POST.get("description", ""),
        instructions=request.POST.get("instructions", ""),
        created_by=request.user,
        status=request.POST.get("status", "draft"),
        max_score=int(request.POST.get("max_score", 100)),
        passing_score=int(request.POST.get("passing_score", 60)),
    )
    
    due_date = request.POST.get("due_date", "").strip()
    if due_date:
        try:
            from datetime import datetime
            assessment.due_date = datetime.fromisoformat(due_date)
            assessment.save()
        except ValueError:
            pass
    
    messages.success(request, f"Assessment '{assessment.title}' created successfully!")
    return redirect("staff_assessments")


# =========================
# PUBLISH ASSESSMENT
# =========================
@login_required
@require_POST
def publish_assessment(request, pk):
    if request.user.profile.role != "staff":
        return render(request, "unauthorized.html")
    
    assessment = get_object_or_404(Assessment, id=pk)
    assessment.status = 'published'
    assessment.save()
    
    messages.success(request, f"Assessment '{assessment.title}' published!")
    return redirect("staff_assessments")


# =========================
# DELETE ASSESSMENT
# =========================
@login_required
@require_POST
def delete_assessment(request, pk):
    if request.user.profile.role != "staff":
        return render(request, "unauthorized.html")
    
    assessment = get_object_or_404(Assessment, id=pk)
    title = assessment.title
    assessment.delete()
    
    messages.success(request, f"Assessment '{title}' deleted.")
    return redirect("staff_assessments")


# =========================
# VIEW SUBMISSIONS
# =========================
@login_required
def view_submissions(request, pk):
    if request.user.profile.role != "staff":
        return render(request, "unauthorized.html")
    
    assessment = get_object_or_404(Assessment, id=pk)
    
    return render(request, "staff_submissions.html", {
        "assessment": assessment,
        "submissions": assessment.submissions.select_related('student').all()
    })


# =========================
# STAFF STUDENTS BY CLASS
# =========================
@login_required
def staff_students(request):
    if request.user.profile.role != "staff":
        return render(request, "unauthorized.html")
    
    # Get all students
    students = User.objects.filter(
        profile__role='student'
    ).select_related('profile').prefetch_related('enrollment_set', 'chatsession_set')
    
    selected_class = request.GET.get('class', None)
    
    # Get unique classes
    classes = list(students.values_list('profile__student_class', flat=True).distinct())
    classes = [c for c in classes if c]  # Remove None values
    
    # Filter by selected class if provided
    if selected_class:
        if selected_class == 'None':
            students = students.filter(profile__student_class__isnull=True)
        else:
            students = students.filter(profile__student_class=selected_class)
    
    # Group students by class
    students_by_class = defaultdict(list)
    for student in students:
        class_name = student.profile.student_class or "Unassigned"
        students_by_class[class_name].append(student)
    
    # Sort classes alphabetically
    students_by_class = dict(sorted(students_by_class.items()))
    
    # Stats
    one_week_ago = timezone.now() - timedelta(days=7)
    
    return render(request, "staff_students.html", {
        "students_by_class": students_by_class,
        "classes": classes,
        "selected_class": selected_class,
        "total_students": students.count() if not selected_class else User.objects.filter(profile__role='student').count(),
        "total_classes": len(classes),
        "complete_profiles": User.objects.filter(profile__role='student', profile__is_profile_complete=True).count(),
        "active_this_week": ChatSession.objects.filter(created_at__gte=one_week_ago).values('student').distinct().count(),
    })
