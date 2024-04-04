from django.conf import settings
from . import views
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
    path('leaderboard',views.leaderboard, name="leaderboard"),
    path('createassignment',views.createassignment, name="createassignment"),
    path('viewassignment/<int:assignment_id>/', views.viewassignment, name='viewassignment'),
    path('submitassignment/<int:assignment_id>/', views.submitassignment, name='submitassignment'),
    path('viewsubmissions', views.viewsubmissions, name='viewsubmissions'),
    path('gradeassignments/<int:assignment_id>/', views.gradeassignments, name='gradeassignments'),
    path("scoreassignment/<int:submission_id>/", views.scoreassignment, name="scoreassignment"),    
    path('createquiz', views.createquiz, name='createquiz'),
    path('viewquiz/<str:course_name>/', views.viewquiz, name='viewquiz'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('submitquiz/<int:quiz_id>/', views.submitquiz, name='submitquiz'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
