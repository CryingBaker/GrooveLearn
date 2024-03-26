from django.db import models
from django.utils import timezone

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField(default=timezone.now)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)

    def __str__(self):
        return self.title
