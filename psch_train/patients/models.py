from django.db import models
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

