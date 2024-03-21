from . import views
from django.urls import path

urlpatterns = [
    path('courses',views.courses, name="courses"),
    path('viewcourses/<str:course_name>',views.viewcourses, name="viewcourses"),
]