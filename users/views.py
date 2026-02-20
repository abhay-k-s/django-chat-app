from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            user.is_online = True
            user.save()
            return redirect('user_list')
    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username,email=email,password=password)
        return redirect('login')
    return render(request, 'register.html')
    

@login_required
def logout_view(request):
    request.user.is_online = False
    request.user.last_seen = timezone.now()
    request.user.save()
    logout(request)
    return redirect('login')