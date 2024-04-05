from django.shortcuts import render

from authentication.models import Teacher
from .models import Course
from assessment.views import listassignments

def get_user_role(user):
    if hasattr(user, 'student'):
        return 'Student'
    elif hasattr(user, 'teacher'):
        return 'Teacher'
    else:
        return 'Unknown'
    
def courses(request):
    user_role = get_user_role(request.user)
    if user_role == 'Teacher':
        all_courses = request.user.teacher.courses.all()
    else:
        all_courses = request.user.student.courses.all()

    teacher_names = {}
    for course in all_courses:
        teachers = Teacher.objects.filter(courses=course)
        print(f"Teachers for course {course.title}: {teachers}")  # Debug print statement
        teacher = teachers.first()
        if teacher:
            teacher_names[course.title] = teacher.user.username

    print(f"Teacher names: {teacher_names}")  # Debug print statement

    return render(request, 'courses/courses.html', {'courses': all_courses, 'teacher_names': teacher_names})

def viewcourses(request, course_name):  
    assignments = listassignments(request, course_name)
    course = Course.objects.get(title=course_name)
    user_role = get_user_role(request.user)
    is_teacher_of_course = False
    if user_role == 'Teacher' and course in request.user.teacher.courses.all():
        is_teacher_of_course = True
    return render(request, 'courses/viewcourses.html',{'course':course, 'is_teacher_of_course':is_teacher_of_course, 'assignments':assignments})

