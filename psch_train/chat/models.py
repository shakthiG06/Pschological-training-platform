from django.db import models
from django.contrib.auth.models import User
from patients.models import PatientScenario

class ChatSession(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientScenario, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.patient.name}"


class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    sender = models.CharField(
        max_length=10,
        choices=[('student', 'Student'), ('patient', 'Patient')]
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message[:30]}"

