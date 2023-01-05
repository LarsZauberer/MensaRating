# pylint: disable=no-member
from django.http import HttpResponse
from django.shortcuts import render  # , redirect
from datetime import datetime as dt  # for date and time
import logging
from .helperFunctions import HelperMenu, getRating, getRatingOfAllTime
from .models import Menu, Review, Image, Rating, Profil


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


def postReview(request, pk):
    log = logging.getLogger("postReview")
    
    # Get the text data from the request body
    data = request.POST.get("text")
    if data is None:
        log.warning(f"No text data received")
        return HttpResponse("No text in body")
    
    # Get the menu
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu not found")
        return HttpResponse("Menu not found")
    menu = menu[0]
    
    # Get the user profil
    profil = None
    if request.user.is_authenticated:
        profil = Profil.objects.get(user=request.user)
    
    Review.objects.create(text=data, profil=profil, menu=menu)
    return HttpResponse("Success!")


def postImage(request, pk):
    # TODO: Implement
    return HttpResponse("")


def postRating(request, pk):
    log = logging.getLogger("postRating")
    
    # Get the rating data from the request body
    data = request.POST.get("rating")
    if data is None:
        log.warning(f"No rating data received")
        return HttpResponse("No rating in body")
    
    try:
        data = int(data)
    except:
        log.warning(f"Received Data is not an integer: {data}")
        return HttpResponse("Invalid")
    
    # Check validity of the rating
    if data > 6 or data < 0:
        return HttpResponse("Invalid")
    
    # Get the menu
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu not found")
        return HttpResponse("Menu not found")
    menu = menu[0]
    
    # Get the user profil
    profil = None
    if request.user.is_authenticated:
        profil = Profil.objects.get(user=request.user)
        
        # Check if the user already has a rating
        log.debug(f"Searching already existing ratings for the user {request.user.username}")
        rating = Rating.objects.filter(menu=menu, profil=profil)
        log.debug(f"Found existing ratings: {rating}")
        if len(rating) == 0:
            log.debug(f"Creating a new rating")
            Rating.objects.create(rating=data, profil=profil, menu=menu)
        else:
            log.debug(f"Changing old rating")
            rating = rating[0]
            rating.rating = data
            rating.save()
    else:
        Rating.objects.create(rating=data, profil=profil, menu=menu)
    
    return HttpResponse("Success!")
