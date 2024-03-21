from django.shortcuts import render
from .models import Course

def courses(request):
    all_courses = Course.objects.all()
    # teachername = all_courses.teacher_name()
    return render(request, 'courses/courses.html',{'courses':all_courses})

def viewcourses(request, course_name):  
    course = Course.objects.get(title=course_name)
    return render(request, 'courses/viewcourses.html',{'course':course})