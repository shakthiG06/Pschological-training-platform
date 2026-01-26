from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Course
from .models import Enrollment


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
