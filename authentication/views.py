from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        print("This works!")
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        password2 = request.POST['c_pass']

                # Check if passwords match
        if password == password2:
                    # Check email
                if User.objects.filter(email=email).exists():
                        print('Email is already taken')
                else:
                        myuser = User.objects.create_user(username,email,password)
                        myuser.name = name
                        myuser.save()
                        print('User created')
                        return redirect('/login')
        else:
            print('Passwords do not match')
    
    return render(request, 'authentication/register.html')

def login(request):
    return render(request, 'authentication/login.html')

def logout(request):
    pass