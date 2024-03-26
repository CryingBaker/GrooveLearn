from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    semester = models.IntegerField(default=1)
    department = models.CharField(max_length=100, default='None')
    roll_no = models.CharField(max_length=100, default='None')
    courses = models.ManyToManyField('courses.Course', blank=True)

    def __str__(self):
        return self.user.username
    

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField('courses.Course', blank=True)

    def __str__(self):
        return self.user.username
