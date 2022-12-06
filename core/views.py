from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime as dt # for date and time
from .helperFunctions import *
from .models import *


def index(request):
    # Get all menus with the date today
    menus = Menu.objects.filter(date=dt.today())
    
    helperMenus = []
    for i in menus:
        helperMenus.append(HelperMenu(i))
    
    # Calculate the rating for each menu
    for i in helperMenus:
        i.rating = getRating(i.menu)
        i.allTimeRating = getRatingOfAllTime(i.menu)
    
    # TODO: Check the webscraper for new menus
    
    return render(request, 'index.html', context={'menus': helperMenus})


def menu(request, pk):
    # Get the menu data
    menu = Menu.objects.get(pk=pk)
    
    # Get the reviews
    reviews = Review.objects.filter(menu=menu)
    
    # Get the images
    images = Image.objects.filter(menu=menu)
    
    # Get the rating
    rating = getRating(menu)
    
    # Calculate the average rating of all time for the menu
    ratingOfAllTime = getRatingOfAllTime(menu)
    
    context = {"menu": menu, "reviews": reviews, "images": images, "rating": rating, "allTimeRating": ratingOfAllTime}  # Create a context dictionary to pass to the template
    
    return render(request, "menu.html", context=context)


def allMenu(request):
    # Get all menus
    menus = Menu.objects.all()
    
    # Delete all multiple occurencies of the same menu
    uniqueMenus = []
    for i in menus:
        # Check if the menu is already in the list
        for e in uniqueMenus:
            if i.name == e.name:  # Is the name of the menu the same?
                break
            else:
                # Add to the unique menus list.
                uniqueMenus.append(i)
    menus = uniqueMenus
    
    # Convert menus to helperMenus
    helperMenus = []
    for i in menus:
        helperMenus.append(HelperMenu(i))
    
    # Calculate all the ratings of all time
    for i in helperMenus:
        i.allTimeRating = getRatingOfAllTime(i.menu)
    
    context = {"menus": helperMenus} # Create a context dictionary to pass to the template
    
    return render(request, "allMenu.html", context=context)


def postReview(request, pk):
    # TODO: Implement
    pass

def postImage(request, pk):
    # TODO: Implement
    pass

def postRating(request, pk):
    # TODO: Implement
    pass
