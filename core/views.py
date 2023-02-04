# pylint: disable=no-member
from django.http import HttpResponse
from django.shortcuts import render  # , redirect
from django.contrib import messages
from datetime import datetime as dt  # for date and time
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
import datetime as dt  # for date and time
from .models import MenuType, Menu, Review, Image, Profil
from .statistic_functions import HelperMenu, getRating, getRatingOfAllTime
from .forms import ImageForm, ReviewForm, RatingForm
from .post_functions import postImage, postRating, postReview
from django.contrib.auth.models import User, Group
from .webscraper import sync_today_menu


def index(request):
    sync_today_menu()

    # Get all menus with the date today
    menus = Menu.objects.filter(date=dt.date.today())

    # Calculate the rating for each menu
    ratings = [getRating(i) for i in menus]
    allTimeRatings = [getRatingOfAllTime(i.menuType) for i in menus]
    
    # Zip all the menu information to one information together.
    # This has to happen, because the rating is not directly saved in the database object.
    menus = zip(menus, ratings, allTimeRatings)

    

    return render(request, 'index.html', context={'menus': menus})


def menu(request, pk):
    sync_today_menu()
    log = logging.getLogger("menu")
    
    # Get the menu data
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu with pk:{pk} not found")
        return HttpResponse("Menu not found")
    menu = menu[0]
    
    today = menu.date == dt.date.today() # Save if the menu is a menu of today
    
    # Check if the request is a post request
    if request.method == "POST" and today:
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
        
        # Return user alert message
        if msg[1] == 1:
            messages.error(request, msg[0])
        else:
            messages.success(request, msg[0])

    # Get the reviews
    reviews = Review.objects.filter(menu=menu)

    # Get the images
    images = Image.objects.filter(menu=menu)

    # Get the rating
    rating = getRating(menu)

    # Calculate the average rating of all time for the menu
    ratingOfAllTime = getRatingOfAllTime(menu.menuType)


    

    # Forms
    imageForm = ImageForm()
    reviewForm = ReviewForm()
    ratingForm = RatingForm()

    context = {"menu": menu, "reviews": reviews, "images": images, "rating": rating,
               "allTimeRating": ratingOfAllTime, "imageForm": imageForm, "reviewForm": reviewForm,
               "ratingForm": ratingForm, "today": today}  # Create a context dictionary to pass to the template

    return render(request, "menu.html", context=context)

def menuType(request, pk):
    sync_today_menu()
    log = logging.getLogger("menuType")
    
    menutype = MenuType.objects.filter(pk=pk)
    if len(menutype) == 0:
        log.warning(f"Menutype with pk:{pk} not found")
        return HttpResponse("Menutype not found")
    menutype = menutype[0]

    menu_instances = Menu.objects.filter(name=menutype.name).order_by("-date")


    description = menu_instances[0].description
    vegetarian = menu_instances[0].vegetarian
    vegan = menu_instances[0].vegan


    occurrences = menu_instances.count()
    allTimeRating = getRatingOfAllTime(menutype)


    context = {"name": menutype.name, "description": description, "vegetarian": vegetarian, "vegan": vegan, "menu_instances": menu_instances[:600], "occurrences": occurrences, "allTimeRating": allTimeRating}

    return render(request, "menuType.html", context=context)



""" def allMenu(request):
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

    return render(request, "allMenu.html", context=context) """


def allMenu(request):
    sync_today_menu()
    
    menuTypes = MenuType.objects.all()
    
    occurrences = []
    allTimeRatings = []

    for typ in menuTypes:
        menus = Menu.objects.filter(name=typ.name)
        occurrences.append(menus.count())
        allTimeRatings.append(getRatingOfAllTime(typ))

    menuType_info = zip(menuTypes, occurrences, allTimeRatings)


    #Order by number of occurrences
    menuType_info = sorted(menuType_info, key=lambda x: x[1], reverse=True)  # Sort the menu info after occurrences -> lowest to highest

    context = {"menuTypes": menuType_info}
   

    return render(request, "allMenu.html", context=context)


def timeline(request):
    sync_today_menu()
    
    menus = Menu.objects.all().order_by("-date")

    context = {"menus": menus[:600]}  # Return the first 600 menus


    return render(request, "timeline.html", context=context)


def userProfile(request):
    sync_today_menu()
    
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    
    profil = Profil.objects.get(user=request.user)

    context = {"name": profil.user, "karma": profil.karma}

    return render(request, "userProfile.html", context=context)
