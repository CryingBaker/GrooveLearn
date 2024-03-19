from . import views
from django.urls import path

urlpatterns = [
    path('leaderboard',views.leaderboard, name="leaderboard"),
]