import logging
from .models import Review, Profil, Rating, Image, Menu
from .forms import ImageForm, ReviewForm, RatingForm


def postReview(request, pk, form):
    log = logging.getLogger("postReview")
    
    # Create Review Object
    if not form.is_valid():
        return "Invalid Form"
    
    review = form.instance
    
    # Get the menu
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu not found")
        return "Menu not found"
    menu = menu[0]
    
    # Get the user profil
    profil = None
    if request.user.is_authenticated:
        profil = Profil.objects.get(user=request.user)
    
    review.menu = menu
    review.profil = profil
    review.save()
    return "Success!"


def postImage(request, pk, form):
    log = logging.getLogger("postImage")
    data = request.POST
    log.debug(f"Image Data: {data}")
    return ""


def postRating(request, pk, form):
    log = logging.getLogger("postRating")
    
    # Check if form valid
    if not form.is_valid():
        return "Invalid Form"
    
    # Get the menu
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu not found")
        return "Menu not found"
    menu = menu[0]
    
    # Get the user profil
    profil = None
    if request.user.is_authenticated:
        profil = Profil.objects.get(user=request.user)
        
        # Check if the user already has a rating
        log.debug(f"Searching already existing ratings for the user {request.user.username}")
        rating = Rating.objects.filter(menu=menu, profil=profil)
        log.debug(f"Found existing ratings: {rating}")
        
        # Change the old rating if there is an old rating
        if len(rating) > 0:
            rating = rating[0]
            rating.rating = form.cleaned_data.get("rating")
            rating.save()
            return "Success!"
    
    # Create rating object
    rating = form.instance
    
    rating.profil = profil
    rating.menu = menu
    rating.save()
    
    return "Success!"
