from django.db import models
from django.contrib.auth.models import User
from chat.models import ChatSession

class Evaluation(models.Model):
    session = models.OneToOneField(ChatSession, on_delete=models.CASCADE)
    staff = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(help_text="Score out of 10")
    feedback = models.TextField()
    approved = models.BooleanField(default=False)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation - {self.session.student.username}"
