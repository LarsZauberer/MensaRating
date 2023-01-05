# pylint: disable=no-member
from django.shortcuts import render  # , redirect
from datetime import datetime as dt  # for date and time
from .helperFunctions import HelperMenu, getRating, getRatingOfAllTime
from .models import Menu, Review, Image
from django.contrib.auth.models import User, Group


def index(request):
    # Get all menus with the date today
    menus = Menu.objects.filter(date=dt.now())

    # Calculate the rating for each menu
    ratings = [getRating(i) for i in menus]
    allTimeRatings = [getRatingOfAllTime(i) for i in menus]
    
    # Zip all the menu information to one information together.
    # This has to happen, because the rating is not directly saved in the database object.
    menus = zip(menus, ratings, allTimeRatings)

    # TODO: Check the webscraper for new menus

    return render(request, 'index.html', context={'menus': menus})


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

    context = {"menu": menu, "reviews": reviews, "images": images, "rating": rating,
               "allTimeRating": ratingOfAllTime}  # Create a context dictionary to pass to the template

    return render(request, "menu.html", context=context)


def allMenu(request):
    # Get all menus
    menu_names = Menu.objects.values("name").distinct()  # Get all unique names for the menus
    
    # Get one menu object of all the menus with the same name
    menus = []
    for i in menu_names:
        menus += Menu.objects.filter(name=i["name"])[:1]  # Get only one menu object back

    # Calculate all the ratings of all time
    allTimeRatings = [getRatingOfAllTime(i) for i in menus]
    
    # Zip menu information together
    menus = zip(menus, allTimeRatings)

    # Create a context dictionary to pass to the template
    context = {"menus": menus}

    return render(request, "allMenu.html", context=context)

def userProfile(request):

    name = request.user.username
    context = {"name": name}

    return render(request, "userProfile.html", context=context)


def postReview(request, pk):
    # TODO: Implement
    pass


def postImage(request, pk):
    # TODO: Implement
    pass


def postRating(request, pk):
    # TODO: Implement
    pass
