from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ('student', 'Student'),
            ('staff', 'Staff')
        ],
        default='student'
    )
    
    # Student details
    institution = models.CharField(max_length=200, blank=True, null=True)
    student_class = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Class A, Section B")
    place = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar_color = models.CharField(max_length=20, default='rose')
    
    # Profile completion tracking
    is_profile_complete = models.BooleanField(default=False)
    show_help = models.BooleanField(default=True)  # Show help dashboard for new users
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ['student_class', 'user__username']

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def get_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = ['institution', 'student_class', 'place', 'phone', 'bio']
        filled = sum(1 for f in fields if getattr(self, f))
        return int((filled / len(fields)) * 100)
