from . import views
from django.urls import path

urlpatterns = [
    path('ranking',views.ranking, name="ranking"),
]