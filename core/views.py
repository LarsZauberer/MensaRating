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
from .statistic_functions import *
from .forms import ImageForm, ReviewForm, RatingForm
from .post_functions import postImage, postRating, postReview
from django.contrib.auth.models import User, Group
from .webscraper import sync_today_menu


def index(request):
    sync_today_menu()

    # Get all menus with the date today
    menus = Menu.objects.filter(date__gte=dt.date.today(), date__lte=dt.date.today() + dt.timedelta(days=7)).order_by("date")  # gte = greater than or equal
    
    dates = []
    menus_with_date = []
    for i, menu in enumerate(menus):
        # Check if the date, when a menu occured is already listed 
        if menu.date not in dates:
            dates.append(menu.date)
            menus_with_date.append([])
        
        # Get best image of the menu
        img = get_all_images_sorted(menu.menuType)
        if img != None:
            img = img[0]
        
        # Add the menu to the list with all the informations
        menus_with_date[-1].append( (i, menu, img, getRating(menu), getNumRates(menu)) )

    # Zip the data together
    menus = zip(dates, menus_with_date)

    context = {'menus_dates': list(menus)}

    return render(request, 'index.html', context=context)


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
    reviews = Review.objects.filter(menu=menu).order_by("-likes")
    review_badges = []
    for i in reviews:
        if i.profil:
            review_badges.append(get_badges_of_profil(i.profil))
        else:
            review_badges.append([])

    # Get the images
    images = Image.objects.filter(menu=menu).order_by("-likes")
    image_badges = []
    for i in images:
        if i.profil:
            image_badges.append(get_badges_of_profil(i.profil))
        else:
            image_badges.append([])
    
    reviews = list(zip(reviews, review_badges))
    images = list(zip(images, image_badges))

    # Get the rating
    rating = getRating(menu)
    numRates = getNumRates(menu)
    

    # Forms
    imageForm = ImageForm()
    reviewForm = ReviewForm()
    ratingForm = RatingForm()

    context = {"menu": menu, "reviews": reviews, "images": images, "rating": rating, "numRates": numRates,
                "imageForm": imageForm, "reviewForm": reviewForm,
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

    menu_instances = Menu.objects.filter(name=menutype.name).filter(date__lte=dt.date.today()).order_by("-date")
    


    description = menu_instances[0].description
    vegetarian = menu_instances[0].vegetarian
    vegan = menu_instances[0].vegan

    
    occurrences = menu_instances.count()
    allTimeRating = getRatingOfAllTime(menutype)
    allTimeNumRates = getNumRatesOfAllTime(menutype)


    ratings = [getRating(i) for i in menu_instances]
    numRates = [getNumRates(i) for i in menu_instances]
    indexes = list(range(len(menu_instances)))

    images = get_all_images_sorted(menutype)
    if images == None: images = []
    image_badges = []
    for i in images:
        if i.profil:
            image_badges.append(get_badges_of_profil(i.profil))
        else:
            image_badges.append([])
    images = list(zip(images, image_badges))





    menu_instances = zip(indexes[:600], ratings[:600], numRates[:600], menu_instances[:600])

    context = {"name": menutype.name, "description": description, "images": images, "vegetarian": vegetarian, "vegan": vegan, "menu_instances": menu_instances, "occurrences": occurrences, "allTimeRating": allTimeRating, "allTimeNumRates": allTimeNumRates}

    return render(request, "menuType.html", context=context)




def allMenu(request):
    sync_today_menu()
    
    menuTypes = MenuType.objects.all()
    
    occurrences = []
    allTimeRatings = []
    allTimeNumRates = []
    descriptions = []
    vegetarians = []
    vegans = []

    for typ in menuTypes:
        menus = Menu.objects.filter(name=typ.name).filter(date__lte=dt.date.today())
        if len(menus) > 0:
            descriptions.append(menus[0].description)
            vegetarians.append(menus[0].vegetarian)
            vegans.append(menus[0].vegan)
            occurrences.append(menus.count())
            allTimeRatings.append(getRatingOfAllTime(typ))
            allTimeNumRates.append(getNumRatesOfAllTime(typ))
        
    indexes = list(range(len(menuTypes))) 

    menuType_info = zip(indexes, menuTypes, occurrences, descriptions, vegetarians, vegans, allTimeRatings, allTimeNumRates)


    #Order by number of occurrences
    #menuType_info = sorted(menuType_info, key=lambda x: x[2], reverse=True)  # Sort the menu info after occurrences -> lowest to highest

    context = {"menuTypes": menuType_info}


    
   

    return render(request, "allMenu.html", context=context)


def timeline(request):
    sync_today_menu()
    menus = Menu.objects.filter(date__lte=dt.date.today()).order_by("-date")
    
    dates = []
    menus_with_date = []
    for i, menu in enumerate(menus):
        if menu.date not in dates:
            dates.append(menu.date)
            menus_with_date.append([])
        

        menus_with_date[-1].append( (i, menu, getRating(menu), getNumRates(menu)) )

    menu_dates = zip(dates[:600], menus_with_date[:600]) # Return the first 600 menus


    context = {"menu_dates": menu_dates}  


    return render(request, "timeline.html", context=context)


def userProfile(request):
    sync_today_menu()
    
    if not request.user.is_authenticated:
        return redirect(reverse("login"))
    
    profil = Profil.objects.get(user=request.user)
    
    badges = get_badges_of_profil(profil)
    
    all_badges = []
    for i in range(3): # 3 Badge categories
        all_badges.append(list(Badge.objects.filter(condition_category=i).order_by("count")))
        
    for i in all_badges:
        for e, el in enumerate(i):
            i[e] = (el, el in badges)  # Tag all the badges the profil posses
    
    reviews = Review.objects.filter(profil=profil).order_by("-likes")
    images = Image.objects.filter(profil=profil).order_by("-likes")

    context = {"name": profil.user, "karma": profil.karma, "badges": all_badges, "images": images, "reviews": reviews}

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
        
    if post.profil is not None:
        post.profil.karma += weight
        post.profil.save()
    
    post.save()  # Save to the database
    
    return HttpResponse(post.likes)
