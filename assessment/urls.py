from . import views
from django.urls import path

urlpatterns = [
    path('leaderboard',views.leaderboard, name="leaderboard"),
    path('createassignment',views.createassignment, name="createassignment"),
]