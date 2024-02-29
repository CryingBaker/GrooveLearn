from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'authentication/home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        password2 = request.POST['c_pass']
        if password == password2:
                if User.objects.filter(email=email).exists():
                        print('Email is already taken')
                else:
                        myuser = User.objects.create_user(username,email,password)
                        myuser.name = name
                        myuser.save()
                        messages.success(request, 'Your account has been created successfully')
                        return redirect('/login')
        else:
            print('Passwords do not match')
    
    return render(request, 'authentication/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['username'] = user.username 
            return render(request, 'authentication/home.html')
        else:
            messages.error(request, 'Invalid credentials, please try again')
            return redirect('/login')
    return render(request, 'authentication/login.html')

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('/login') 

def profile(request):
    return render(request, 'authentication/profile.html')