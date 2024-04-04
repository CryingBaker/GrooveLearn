import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Assignment, AssignmentSubmission, Quiz, MCQQuestion, MCQChoice, QuizSubmission
from courses.models import Course
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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
        user_role = get_user_role(request.user)
        if user_role == 'Teacher':
            courses = request.user.teacher.courses.all()
        else:
            courses = Course.objects.none()  
        return render(request, 'assessment/createassignment.html', {'courses': courses})
    
def listassignments(request, course_name):
    user_role = get_user_role(request.user)
    if user_role == 'Student':
        courses = request.user.student.courses.all()
    elif user_role == 'Teacher':
        courses = request.user.teacher.courses.all()
    else:
        courses = Course.objects.all()
    course = Course.objects.get(title=course_name)
    assignments = Assignment.objects.filter(course=course).order_by('-id')
    return assignments

def viewassignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    try:
        submission = AssignmentSubmission.objects.get(assignment=assignment_id, user=request.user)
        score = submission.score
    except AssignmentSubmission.DoesNotExist:
        score = None
        submission = None
    return render(request, 'assessment/viewassignment.html', {'assignment': assignment,'score': score,'submission': submission})

def submitassignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        try:
            submission = AssignmentSubmission.objects.get(user=request.user, assignment=assignment)
            submission.file = uploaded_file
        except AssignmentSubmission.DoesNotExist:
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

def createquiz(request):
    user_role = get_user_role(request.user)
    if user_role == 'Teacher':
        courses = request.user.teacher.courses.all()
    else:
        courses = Course.objects.none()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)
        typeofquiz=request.POST.get('quiz_type')
        total_points = 0

        quiz = Quiz.objects.create(
            title=title,
            description=description,
            course=course,
            type=typeofquiz,
        )

        difficulty_points = {
            'easy': 1,
            'medium': 3,
            'hard': 5
        }

        questions_data = request.POST.get('questions')
        if questions_data is not None:
            questions_data = json.loads(questions_data)
            questions = questions_data.get('questions')
            print(f'Parsed questions_data: {questions}') 
            if isinstance(questions, list):
                try:
                    for question_data in questions:
                        question_text = question_data['question_text']
                        difficulty = question_data['difficulty']
                        question = MCQQuestion.objects.create(
                            question_text=question_text,
                            quiz=quiz,
                            level=difficulty
                        )
                        total_points += difficulty_points.get(difficulty, 0)
                        for choice_data in question_data['choices']:
                            choice_text = choice_data['choice_text']
                            is_correct = choice_data['is_correct']
                            MCQChoice.objects.create(
                                choice_text=choice_text,
                                is_correct=is_correct,
                                question=question
                            )
                    quiz.totalpoints = total_points
                    quiz.totalquestions = len(questions)
                    quiz.save()
                except Exception as e:
                    print(f'Error when creating questions and choices: {e}')
            else:
                print(f'Unexpected questions_data: {questions_data}')
                return redirect('/courses')

    return render(request, 'assessment/createquiz.html', {'courses': courses})

def viewquiz(request, course_name):
    course = Course.objects.get(title=course_name)
    quizzes = Quiz.objects.filter(course=course)
    return render(request, 'assessment/viewquiz.html', {'quizzes': quizzes, 'course': course})

def quiz(request, quiz_id, check=0):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if not check==1 and QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists():
        print("1")
        return showresult(request,quiz_id)
    print("0")
    questions = MCQQuestion.objects.filter(quiz=quiz).order_by('?')
    choices = {question: MCQChoice.objects.filter(question=question).order_by('?') for question in questions}
    return render(request, 'assessment/quiz.html', {'quiz': quiz, 'questions': questions, 'choices': choices})

def submitquiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    difficulty_points = {
        'easy': 1,
        'medium': 3,
        'hard': 5
    }
    if request.method == 'POST':
        score = 0
        correct_answers=0
        questions = MCQQuestion.objects.filter(quiz=quiz)
        for question in questions:
            choice_id = request.POST.get('choice_for_question_{}'.format(question.id))
            choice = MCQChoice.objects.filter(id=choice_id).first()
            if choice and choice.is_correct:
                score += difficulty_points.get(question.level, 0)
                correct_answers+=1
        QuizSubmission.objects.create(user=request.user, quiz=quiz, score=score, correctlyanswered=correct_answers)
        return redirect('viewquiz', course_name=quiz.course.title)
    return render(request, 'assessment/quiz.html', {'quiz': quiz})

def getquizscore(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user
    score = QuizSubmission.objects.get(user=user, quiz=quiz).score
    return score

def showresult(request,quiz_id):
    quiz=get_object_or_404(Quiz, id=quiz_id)
    score=getquizscore(request,quiz_id)
    submissions=QuizSubmission.objects.filter(user=request.user, quiz=quiz).first()
    return render(request, 'assessment/result.html',{'quiz':quiz,'score':score, 'submissions':submissions})