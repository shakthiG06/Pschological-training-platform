from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from patients.models import PatientScenario
from chat.models import ChatSession, ChatMessage
from chat.ai_engine import generate_patient_reply
from courses.models import Enrollment


@login_required
def chat_view(request, patient_id):
    patient = PatientScenario.objects.get(id=patient_id)

    # 🔒 Course completion check
    enrolled = Enrollment.objects.filter(
        student=request.user,
        course=patient.course,
        completed=True
    ).exists()

    if not enrolled:
        return render(
            request,
            "access_denied.html",
            {"course": patient.course}
        )

    # Create or get chat session
    session, created = ChatSession.objects.get_or_create(
        student=request.user,
        patient=patient
    )

    if request.method == "POST":
        user_message = request.POST.get("message")

        ChatMessage.objects.create(
            session=session,
            sender="student",
            message=user_message
        )

        ai_reply = generate_patient_reply(
            patient.persona_prompt,
            user_message
        )

        ChatMessage.objects.create(
            session=session,
            sender="patient",
            message=ai_reply
        )

        return redirect("chat", patient_id=patient.id)

    messages = ChatMessage.objects.filter(session=session)

    return render(
        request,
        "chat.html",
        {
            "patient": patient,
            "messages": messages
        }
    )
