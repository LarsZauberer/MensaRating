# pylint: disable=no-member
from django.http import HttpResponse
from django.shortcuts import render  # , redirect
from django.contrib import messages
from datetime import datetime as dt  # for date and time
import logging
from .statistic_functions import HelperMenu, getRating, getRatingOfAllTime
from .models import Menu, Review, Image, Rating, Profil
from .forms import ImageForm, ReviewForm, RatingForm
from .post_functions import postImage, postRating, postReview


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
    log = logging.getLogger("menu")
    
    # Check if the request is a post request
    if request.method == "POST":
        log.debug(f"Post Data received: {request.POST}")
        log.debug(f"Files received: {request.FILES}")
        form = None
        
        # Sort different post kinds
        # Rating
        if request.POST.get("rating"):
            form = RatingForm(request.POST)
            log.debug(f"Rating Form Recognized")
            msg = postRating(request, pk, form)
        
        # Review
        elif request.POST.get("text"):
            form = ReviewForm(request.POST)
            log.debug(f"Review Form Recognized")
            msg = postReview(request, pk, form)
        
        # Image
        elif request.FILES.get("image"):
            form = ImageForm(request.POST, request.FILES)
            log.debug(f"Image Form Recognized")
            msg = postImage(request, pk, form)
        
        # None of the valid kinds
        if form is None:
            log.warning(f"Form type is invalid for post data: {request.POST}")
            msg = ("Invalid Form Type", 1)
        
        if msg[1] == 1:
            messages.error(request, msg[0])
        else:
            messages.success(request, msg[0])
    
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

    # Forms
    imageForm = ImageForm()
    reviewForm = ReviewForm()
    ratingForm = RatingForm()

    context = {"menu": menu, "reviews": reviews, "images": images, "rating": rating,
               "allTimeRating": ratingOfAllTime, "imageForm": imageForm, "reviewForm": reviewForm,
               "ratingForm": ratingForm}  # Create a context dictionary to pass to the template

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
