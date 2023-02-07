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
from .statistic_functions import HelperMenu, getRating, getRatingOfAllTime, getMostLikedImage
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


    images = [getMostLikedImage(i.menuType) for i in menus]
    


    
    # Zip all the menu information to one information together.
    # This has to happen, because the rating is not directly saved in the database object.
    menus = zip(menus, ratings, allTimeRatings, images)

    

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




def allMenu(request):
    sync_today_menu()
    
    menuTypes = MenuType.objects.all()
    
    occurrences = []
    allTimeRatings = []
    descriptions = []
    vegetarians = []
    vegans = []

    for typ in menuTypes:
        menus = Menu.objects.filter(name=typ.name)
        descriptions.append(menus[0].description)
        vegetarians.append(menus[0].vegetarian)
        vegans.append(menus[0].vegan)
        occurrences.append(menus.count())
        allTimeRatings.append(getRatingOfAllTime(typ))

    menuType_info = zip(menuTypes, occurrences, descriptions, vegetarians, vegans, allTimeRatings)


    #Order by number of occurrences
    menuType_info = sorted(menuType_info, key=lambda x: x[1], reverse=True)  # Sort the menu info after occurrences -> lowest to highest

    context = {"menuTypes": menuType_info}
   

    return render(request, "allMenu.html", context=context)


def timeline(request):
    sync_today_menu()

    
    
    menus = Menu.objects.all().order_by("-date")


    dates = []
    menus_with_date = []
    for menu in menus:
        if menu.date not in dates:
            dates.append(menu.date)
            menus_with_date.append([])
        menus_with_date[-1].append(menu)

    menu_dates = zip(dates[:600], menus_with_date[:600]) # Return the first 600 menus


    context = {"menu_dates": menu_dates}  


    return render(request, "timeline.html", context=context)


def userProfile(request):
    sync_today_menu()
    
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    
    profil = Profil.objects.get(user=request.user)

    context = {"name": profil.user, "karma": profil.karma}

    return render(request, "userProfile.html", context=context)


def like(request, cat: int, pk: int):
    log = logging.getLogger("Like View")
    
    # All models that can be liked
    obj_cat: dict = {
        1: Review,
        2: Image
    }
    
    obj = obj_cat.get(cat)
    
    # Is the category index out of range for the dict
    if not obj:
        log.warning(f"Category: {cat} out of range")
        return HttpResponse("Category not found")
    
    log.debug(f"Model recognized: {obj}")
    
    post = obj.objects.filter(pk=pk)  # Get the post object from the database
    
    # If a post found
    if len(post) == 0:
        log.warning(f"No model of type {obj} with pk {pk} found!")
        return HttpResponse("Post not found")

    post = post[0]
    
    # Check if the post is from today
    if post.menu.date != dt.date.today():
        log.warning(f"Post is to old")
        return HttpResponse("Post cannot be liked anymore")
    
    # Check if dislike or like
    dislike = request.GET.get("dislike")
    
    # Check if this should be a dislike
    weight = 1
    if dislike:
        log.debug(f"Dislike: {dislike}")
        weight = -1
    
    # Like the post
    post.likes += weight
    
    # If the like count is below zero -> 0
    if post.likes < 0:
        post.likes = 0
    
    post.save()  # Save to the database
    
    return HttpResponse(post.likes)
