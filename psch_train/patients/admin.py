from django.contrib import admin
from .models import PatientScenario, PatientAssignment

admin.site.register(PatientScenario)


@admin.register(PatientAssignment)
class PatientAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'patient', 'assigned_by', 'assigned_at')
    list_filter = ('assigned_at', 'patient')
    search_fields = ('student__username', 'patient__name')
    raw_id_fields = ('student', 'patient', 'assigned_by')
