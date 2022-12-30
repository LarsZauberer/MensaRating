from django.shortcuts import render  # , redirect
# from django.http import HttpResponse
from datetime import datetime as dt  # for date and time
from .helperFunctions import HelperMenu, getRating, getRatingOfAllTime
from .models import Menu, Review, Image


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

    # Calculate all the ratings of all time
    allTimeRatings = [getRatingOfAllTime(i) for i in menus]
    
    # Zip menu information together
    menus = zip(menus, allTimeRatings)

    # Create a context dictionary to pass to the template
    context = {"menus": menus}

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
