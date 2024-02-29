from django.shortcuts import render

def ranking(request):
    return render(request, 'assessment/ranking.html')