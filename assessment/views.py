from django.shortcuts import render
from .models import Assignment
from courses.models import Course
from django.shortcuts import redirect

def get_user_role(user):
    if hasattr(user, 'student'):
        return 'Student'
    elif hasattr(user, 'teacher'):
        return 'Teacher'
    else:
        return 'Unknown'
    

def leaderboard(request):
    return render(request, 'assessment/leaderboard.html')

def createassignment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        course_id = request.POST.get('course')
        file = request.FILES.get('file')

        course = Course.objects.get(id=course_id)

        Assignment.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            course=course,
            file=file
        )
        return redirect('/courses')
    else:
        courses = Course.objects.all()
        return render(request, 'assessment/createassignment.html', {'courses': courses})
    
def listassignments(request):
    user_role = get_user_role(request.user)
    if user_role == 'Student':
        courses = request.user.student.courses.all()
    elif user_role == 'Teacher':
        courses = request.user.teacher.courses.all()
    else:
        courses = Course.objects.all()

    assignments = Assignment.objects.filter(course__in=courses)
    return assignments