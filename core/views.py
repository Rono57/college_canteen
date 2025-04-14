# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        # Handled by API, redirect after
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def menu(request):
    return render(request, 'menu.html')

@login_required
def orders(request):
    return render(request, 'orders.html')

@login_required
def complaints(request):
    return render(request, 'complaints.html')