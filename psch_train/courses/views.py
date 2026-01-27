from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Course, Enrollment, Quiz, Question, QuizAttempt, QuizAnswer


@login_required
def course_list(request):
    """
    Displays all psychology courses for the student
    with enrollment & completion status.
    """

    courses = Course.objects.all()

    # Get enrollments for this student
    enrollments = Enrollment.objects.filter(student=request.user)

    enrollment_map = {
        e.course_id: e for e in enrollments
    }

    return render(
        request,
        "courses.html",
        {
            "courses": courses,
            "enrollment_map": enrollment_map
        }
    )


@login_required
def course_detail(request, course_id):
    """
    Display course content and quiz access.
    """
    course = get_object_or_404(Course, id=course_id)
    
    # Get or create enrollment
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )
    
    # Get quiz attempt history
    quiz = getattr(course, 'quiz', None)
    attempts = []
    best_attempt = None
    
    if quiz:
        attempts = QuizAttempt.objects.filter(
            student=request.user,
            quiz=quiz
        ).order_by('-started_at')[:5]
        
        best_attempt = QuizAttempt.objects.filter(
            student=request.user,
            quiz=quiz,
            completed_at__isnull=False
        ).order_by('-score').first()
    
    return render(request, "course_detail.html", {
        "course": course,
        "enrollment": enrollment,
        "quiz": quiz,
        "attempts": attempts,
        "best_attempt": best_attempt,
    })


@login_required
def start_quiz(request, course_id):
    """
    Start a new quiz attempt.
    """
    course = get_object_or_404(Course, id=course_id)
    quiz = get_object_or_404(Quiz, course=course)
    
    # Create new attempt
    attempt = QuizAttempt.objects.create(
        student=request.user,
        quiz=quiz,
        total_questions=quiz.questions.count()
    )
    
    return redirect('take_quiz', attempt_id=attempt.id)


@login_required
def take_quiz(request, attempt_id):
    """
    Display quiz questions and handle submission.
    """
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    # Check if already completed
    if attempt.completed_at:
        return redirect('quiz_result', attempt_id=attempt.id)
    
    quiz = attempt.quiz
    questions = quiz.questions.prefetch_related('choices').all()
    
    if request.method == 'POST':
        score = 0
        
        for question in questions:
            choice_id = request.POST.get(f'question_{question.id}')
            selected_choice = None
            is_correct = False
            
            if choice_id:
                try:
                    selected_choice = question.choices.get(id=choice_id)
                    is_correct = selected_choice.is_correct
                    if is_correct:
                        score += 1
                except:
                    pass
            
            QuizAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct
            )
        
        # Update attempt
        attempt.score = score
        attempt.completed_at = timezone.now()
        percentage = (score / attempt.total_questions * 100) if attempt.total_questions > 0 else 0
        attempt.passed = percentage >= quiz.passing_score
        attempt.save()
        
        # If passed, mark enrollment as completed
        if attempt.passed:
            enrollment = Enrollment.objects.filter(
                student=request.user,
                course=quiz.course
            ).first()
            if enrollment and not enrollment.completed:
                enrollment.completed = True
                enrollment.completed_at = timezone.now()
                enrollment.save()
                messages.success(request, f'🎉 Congratulations! You passed and completed {quiz.course.title}!')
        
        return redirect('quiz_result', attempt_id=attempt.id)
    
    # Calculate time remaining if time limit exists
    time_remaining = None
    if quiz.time_limit_minutes > 0:
        elapsed = (timezone.now() - attempt.started_at).total_seconds()
        time_remaining = max(0, quiz.time_limit_minutes * 60 - int(elapsed))
    
    return render(request, "quiz.html", {
        "attempt": attempt,
        "quiz": quiz,
        "questions": questions,
        "time_remaining": time_remaining,
    })


@login_required
def quiz_result(request, attempt_id):
    """
    Display quiz results with explanations.
    """
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    if not attempt.completed_at:
        return redirect('take_quiz', attempt_id=attempt.id)
    
    # Get answers with questions and choices
    answers = attempt.answers.select_related(
        'question', 'selected_choice'
    ).order_by('question__order')
    
    # Build results data
    results = []
    for answer in answers:
        correct_choice = answer.question.choices.filter(is_correct=True).first()
        results.append({
            'question': answer.question,
            'selected': answer.selected_choice,
            'correct': correct_choice,
            'is_correct': answer.is_correct,
            'explanation': answer.question.explanation,
        })
    
    percentage = (attempt.score / attempt.total_questions * 100) if attempt.total_questions > 0 else 0
    
    return render(request, "quiz_result.html", {
        "attempt": attempt,
        "quiz": attempt.quiz,
        "results": results,
        "percentage": round(percentage, 1),
    })

