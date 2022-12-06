from django.shortcuts import render, redirect
from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')


def menu(request, pk):
    return render(request, "menu.html")


def allMenu(request):
    return render(request, "allMenu.html")


def postReview(request, pk):
    # TODO: Implement
    pass

def postImage(request, pk):
    # TODO: Implement
    pass

def postRating(request, pk):
    # TODO: Implement
    pass
