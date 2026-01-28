from django.db import models
from django.conf import settings
from chat.models import ChatSession
from django.utils import timezone

class Evaluation(models.Model):
    session = models.OneToOneField(
        ChatSession,
        on_delete=models.CASCADE
    )

    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    communication_score = models.IntegerField(default=0)
    empathy_score = models.IntegerField(default=0)
    clinical_reasoning_score = models.IntegerField(default=0)

    notes = models.TextField(blank=True)
    ai_feedback = models.TextField(blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    evaluated_at = models.DateTimeField(null=True, blank=True)

    @property
    def average_score(self):
        """Calculate average of all three scores"""
        return (self.communication_score + self.empathy_score + self.clinical_reasoning_score) / 3

    @property
    def readiness(self):
        """Determine if student is ready based on average score"""
        if self.average_score >= 7:
            return "Ready"
        return "Needs Practice"

    @property
    def ai_summary(self):
        """Return AI feedback or generate a default summary"""
        if self.ai_feedback:
            return self.ai_feedback
        if self.average_score >= 8:
            return "Excellent performance demonstrating strong clinical skills and empathetic communication."
        elif self.average_score >= 6:
            return "Good foundational skills with room for improvement in some areas."
        else:
            return "Continue practicing to strengthen your therapeutic communication skills."

    def __str__(self):
        return f"Evaluation for Session {self.session.id}"
