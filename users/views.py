from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

def index(request):
    return HttpResponse("Hi users index!!")

def logout_user(request):
    logout(request)
    return redirect("login")