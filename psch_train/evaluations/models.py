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

    def __str__(self):
        return f"Evaluation for Session {self.session.id}"
