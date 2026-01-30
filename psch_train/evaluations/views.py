from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from chat.models import ChatSession
from .models import Evaluation


# ===============================
# STAFF: Evaluate a chat session
# ===============================
@login_required
def evaluate_session(request, session_id):
    # 🔐 Allow only staff users
    if request.user.profile.role != "staff":
        return HttpResponseForbidden("You are not authorized to evaluate.")

    session = get_object_or_404(ChatSession, id=session_id)

    # Prevent duplicate evaluations
    evaluation = Evaluation.objects.filter(session=session).first()
    if evaluation:
        # Staff already evaluated - redirect to staff dashboard with message
        messages.info(request, f"This session has already been evaluated.")
        return redirect("staff_dashboard")

    if request.method == "POST":
        Evaluation.objects.create(
            session=session,
            evaluator=request.user,
            communication_score=int(request.POST.get("communication_score")),
            empathy_score=int(request.POST.get("empathy_score")),
            clinical_reasoning_score=int(request.POST.get("clinical_reasoning_score")),
            notes=request.POST.get("notes"),
            ai_feedback=request.POST.get("ai_feedback"),
        )

        # Redirect staff to dashboard with success message instead of result page
        messages.success(request, f"Evaluation for {session.student.username} submitted successfully!")
        return redirect("staff_dashboard")

    return render(
        request,
        "evaluation.html",
        {
            "session": session
        }
    )


# =====================================
# STUDENT/STAFF: View evaluation result
# =====================================
@login_required
def evaluation_result(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)

    # 🔐 Student can only see THEIR session results, staff can view any evaluated session
    is_owner = session.student == request.user
    is_staff = request.user.profile.role == "staff"
    
    if not (is_owner or is_staff):
        return HttpResponseForbidden("You are not authorized to view this result.")

    evaluation = Evaluation.objects.filter(session=session).first()

    return render(
        request,
        "evaluation_result.html",
        {
            "session": session,
            "evaluation": evaluation,
            "is_staff": is_staff
        }
    )
