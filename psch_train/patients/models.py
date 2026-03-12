from django.db import models
from django.contrib.auth.models import User
from courses.models import Course

class PatientScenario(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    severity = models.CharField(
        max_length=20,
        choices=[
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe')
        ]
    )
    persona_prompt = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.condition}"


class PatientAssignment(models.Model):
    """Allows staff to directly assign students to patient scenarios"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_assignments')
    patient = models.ForeignKey(PatientScenario, on_delete=models.CASCADE, related_name='assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_patients')
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Optional notes about this assignment")

    class Meta:
        unique_together = ('student', 'patient')
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.student.username} -> {self.patient.name}"

