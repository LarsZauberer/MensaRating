from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, World! You're at the core index.")

# Create your views here.
def app(request):
    return HttpResponse("Hello, World! You're at the core app.")
