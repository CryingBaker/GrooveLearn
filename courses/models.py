from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Module(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class MCQQuestion(models.Model):
    question_text = models.TextField()
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    question = models.ForeignKey(MCQQuestion, related_name='choices', on_delete=models.CASCADE)

    def __str__(self):
        return self.choice_text

class Answer(models.Model):
    question = models.OneToOneField(MCQQuestion, on_delete=models.CASCADE)
    correct_choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'Answer for {self.question.question_text}'