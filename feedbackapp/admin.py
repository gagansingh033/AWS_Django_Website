from django.contrib import admin

# Register your models here.
from .models import AddProgramAndFacultyName, SendEmailToTrainer, ExportTrainingFeedbackScore, \
    SendReminder, ExportTableOnSapId, ExportAllDatabase

admin.site.register(AddProgramAndFacultyName)
admin.site.register(SendEmailToTrainer)
admin.site.register(ExportTrainingFeedbackScore)
admin.site.register(SendReminder)
admin.site.register(ExportTableOnSapId)
admin.site.register(ExportAllDatabase)
