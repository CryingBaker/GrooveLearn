from django.contrib import admin

from .models import Course, Module, Assignment, MCQQuestion, Choice, Answer

admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Assignment)
# admin.site.register(Student)
admin.site.register(MCQQuestion)
admin.site.register(Choice)
admin.site.register(Answer)

