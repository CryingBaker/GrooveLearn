from django.contrib import admin
from .models import Assignment,AssignmentSubmission,Quiz,MCQQuestion,MCQChoice,QuizSubmission

admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Quiz)
admin.site.register(MCQQuestion)
admin.site.register(MCQChoice)
admin.site.register(QuizSubmission)
