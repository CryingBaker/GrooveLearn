from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Assignment, AssignmentSubmission
from courses.models import Course
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage

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

def viewassignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    try:
        submission = AssignmentSubmission.objects.get(assignment=assignment_id, user=request.user)
        score = submission.score
    except AssignmentSubmission.DoesNotExist:
        score = None
    return render(request, 'assessment/viewassignment.html', {'assignment': assignment,'score': score})

def submitassignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        submission = AssignmentSubmission(user=request.user, assignment=assignment, file=uploaded_file)
        submission.save()
        return redirect('viewassignment', assignment_id=assignment_id)
    return render(request, 'assessment/viewassignment.html', {'assignment': assignment})

def viewsubmissions(request):
    courses = request.user.teacher.courses.all()
    assignments = Assignment.objects.filter(course__in=courses)
    return render(request, 'assessment/viewsubmissions.html', {'assignments': assignments})

def gradeassignments(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    return render(request, 'assessment/gradeassignments.html', {'submissions': submissions, 'assignment': assignment})

def scoreassignment(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)
    if request.method == 'POST':
        score = request.POST.get('grade')
        submission.score = score
        submission.save()
        return redirect('gradeassignments', assignment_id=submission.assignment.id)
    return render(request, 'assessment/scoreassignments.html', {'submission': submission})