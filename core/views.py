from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def menu(request):
    return render(request, "menu.html")


def allMenu(request):
    return render(request, "allMenu.html")
