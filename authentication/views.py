from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password

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
                        myuser.first_name = name
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

def updateprofile(request):
    if request.method == 'POST':
        newusername = request.POST['username']
        newemail = request.POST['email']
        oldpassword = request.POST['old_pass']
        newpassword = request.POST.get('pass')
        newpassword2 = request.POST['c_pass']
        if newusername:
            request.user.username = newusername
        if newemail:
            if User.objects.filter(email=newemail).exists():
                messages.error(request, 'Email is already taken')
            else:
                request.user.email = newemail

        if check_password(oldpassword, request.user.password) and newpassword is not None and newpassword2 is not None:
            if newpassword == newpassword2:
                request.user.set_password(newpassword)
            else:
                messages.error(request, 'Passwords do not match')
        request.user.save()
        update_session_auth_hash(request, request.user)
        messages.success(request, 'Profile updated successfully')
        return redirect('profile')
    return render(request, 'authentication/updateprofile.html')

    
