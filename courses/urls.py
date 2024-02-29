from . import views
from django.urls import path

urlpatterns = [
    path('courses',views.courses, name="courses"),
]