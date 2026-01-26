from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from patients.models import PatientScenario
from chat.models import ChatSession, ChatMessage
from chat.ai_engine import generate_patient_reply
from courses.models import Enrollment


@login_required
def chat_home(request):
    """
    Landing page for /chat/
    Shows all AI patient scenarios unlocked for the student
    based on completed courses.
    """

    # Get all completed courses for the logged-in student
    completed_courses = Enrollment.objects.filter(
        student=request.user,
        completed=True
    ).values_list("course", flat=True)

    # Fetch patient scenarios linked to completed courses
    patients = PatientScenario.objects.filter(
        course__in=completed_courses
    )

    return render(
        request,
        "chat_home.html",
        {
            "patients": patients
        }
    )


@login_required
def chat_view(request, patient_id):
    """
    Handles AI-simulated patient chat for psychology training.
    Students must complete the related course before accessing the chat.
    """

    # 1️⃣ Fetch patient scenario safely
    patient = get_object_or_404(PatientScenario, id=patient_id)

    # 2️⃣ 🔒 Check course completion (MANDATORY)
    has_completed_course = Enrollment.objects.filter(
        student=request.user,
        course=patient.course,
        completed=True
    ).exists()

    if not has_completed_course:
        # Block access if course not completed
        return render(
            request,
            "access_denied.html",
            {
                "course": patient.course,
                "patient": patient
            }
        )

    # 3️⃣ Get or create chat session (one per student + patient)
    session, _ = ChatSession.objects.get_or_create(
        student=request.user,
        patient=patient
    )

    # 4️⃣ Handle student message
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip()

        if user_message:
            # Save student message
            ChatMessage.objects.create(
                session=session,
                sender="student",
                message=user_message
            )

            # Generate AI patient reply using persona prompt
            ai_reply = generate_patient_reply(
                persona_prompt=patient.persona_prompt,
                user_message=user_message
            )

            # Save AI reply
            ChatMessage.objects.create(
                session=session,
                sender="patient",
                message=ai_reply
            )

        # Redirect to prevent duplicate submissions
        return redirect("chat", patient_id=patient.id)

    # 5️⃣ Fetch full conversation history
    messages = ChatMessage.objects.filter(
        session=session
    ).order_by("timestamp")

    # 6️⃣ Render chat UI
    return render(
        request,
        "chat.html",
        {
            "patient": patient,
            "messages": messages,
            "session": session
        }
    )
