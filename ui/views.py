from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse

def logout_view(request):
    logout(request)
    return HttpResponse("Logged out")

def login_view(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("Login "+username)
    else:
        return HttpResponse("Invalid login")

def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Hello "+request.user.username)
    else:
        return HttpResponse("Who are you")