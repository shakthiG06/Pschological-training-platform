from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from patients.models import PatientScenario, PatientAssignment
from chat.models import ChatSession, ChatMessage
from chat.ai_engine import generate_patient_reply
from courses.models import Enrollment


@login_required
def chat_home(request):
    """
    Landing page for /chat/
    Shows all AI patient scenarios unlocked for the student
    based on completed courses OR direct staff assignments.
    """

    # Get all completed courses for the logged-in student
    completed_courses = Enrollment.objects.filter(
        student=request.user,
        completed=True
    ).values_list("course", flat=True)

    # Fetch patient scenarios linked to completed courses
    patients_from_courses = PatientScenario.objects.filter(
        course__in=completed_courses
    )
    
    # Fetch patient scenarios directly assigned by staff
    assigned_patient_ids = PatientAssignment.objects.filter(
        student=request.user
    ).values_list("patient_id", flat=True)
    
    patients_from_assignments = PatientScenario.objects.filter(
        id__in=assigned_patient_ids
    )
    
    # Combine both querysets (union to avoid duplicates)
    patients = (patients_from_courses | patients_from_assignments).distinct()

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
    Students must complete the related course OR be assigned by staff.
    """

    # 1️⃣ Fetch patient scenario safely
    patient = get_object_or_404(PatientScenario, id=patient_id)

    # 2️⃣ 🔒 Check course completion OR staff assignment
    has_completed_course = Enrollment.objects.filter(
        student=request.user,
        course=patient.course,
        completed=True
    ).exists()
    
    has_staff_assignment = PatientAssignment.objects.filter(
        student=request.user,
        patient=patient
    ).exists()

    if not has_completed_course and not has_staff_assignment:
        # Block access if neither course completed nor assigned
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

            # Build conversation history for context (exclude the message we just saved)
            all_messages = list(ChatMessage.objects.filter(
                session=session
            ).order_by("timestamp"))
            history_messages = all_messages[:-1] if len(all_messages) > 1 else []
            
            conversation_history = []
            for msg in history_messages:
                role = "user" if msg.sender == "student" else "assistant"
                conversation_history.append({
                    "role": role,
                    "content": msg.message
                })

            # Generate AI patient reply using persona prompt with history
            ai_reply = generate_patient_reply(
                persona_prompt=patient.persona_prompt,
                user_message=user_message,
                conversation_history=conversation_history
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
