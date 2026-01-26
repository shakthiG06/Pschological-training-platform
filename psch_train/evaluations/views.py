from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from chat.models import ChatSession
from .models import Evaluation

@login_required
def evaluate_session(request, session_id):
    # Allow only staff
    if request.user.profile.role != "staff":
        return HttpResponseForbidden("You are not authorized to evaluate.")

    session = ChatSession.objects.get(id=session_id)

    if request.method == "POST":
        Evaluation.objects.create(
            session=session,
            staff=request.user,
            score=request.POST.get("score"),
            feedback=request.POST.get("feedback"),
            approved=request.POST.get("approved") == "on"
        )
        return redirect("/admin/")

    return render(request, "evaluation.html", {"session": session})
