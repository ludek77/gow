from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse

def logout_view(request):
    logout(request)
    return HttpResponse("Logged out")

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('OK')
    else:
        return HttpResponse('Invalid username or password', status=401)

def index(request):
    return render(request, 'index.html')
