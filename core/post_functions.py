# Maintained by: Robin, Ian
import logging
from .models import Review, Profil, Rating, Image, Menu
from .forms import ImageForm, ReviewForm, RatingForm


def postReview(request, pk, form):
    log = logging.getLogger("postReview")
    log.debug("posting review")
    
    # Create Review Object
    if not form.is_valid():
        log.warning(f"Invalid Form")
        return ("Invalid Form", 1)
    
    review = form.instance
    
    # Get the menu
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu not found")
        return ("Menu not found", 1)
    menu = menu[0]
    
    # Get the user profil
    profil = None
    if request.user.is_authenticated:
        profil = Profil.objects.get(user=request.user)
    
    # Save the context information
    review.menu = menu
    review.profil = profil
    review.save()
    
    # Add Karma
    add_karma_for_posting(review)
    return ("Kommentar erfolgreich gepostet!", 0)


def postImage(request, pk, form):
    log = logging.getLogger("postImage")
    log.debug("posting image")
    
    # Check if form valid
    if not form.is_valid():
        log.warning(f"Invalid Form")
        return ("Invalid Form", 1)
    
    # Get the menu
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu not found")
        return ("Menu not found", 1)
    menu = menu[0]
    
    # Get the user profil
    profil = None
    if request.user.is_authenticated:
        profil = Profil.objects.get(user=request.user)
    
    # Save the context information
    image = form.instance
    image.menu = menu
    image.profil = profil
    image.save()

    # Add Karma
    add_karma_for_posting(image)
    
    return ("Bild erfolgreich hochgeladen!", 0)


def postRating(request, pk, form):
    log = logging.getLogger("postRating")
    log.debug(f"posting rating")
    
    # Check if form valid
    if not form.is_valid():
        log.warning(f"Invalid Form")
        return ("Invalid Form", 1)
    
    # Get the menu
    menu = Menu.objects.filter(pk=pk)
    if len(menu) == 0:
        log.warning(f"Menu not found")
        return ("Menu not found", 1)
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
            if rating.rating > 1:
                sing_plur = "Sternen"
            else:
                sing_plur = "Stern"
            return ("Menü mit " + str(rating.rating) + " " + sing_plur +" bewertet!", 0)
    
    # Create rating object
    rating = form.instance
    
    # Save the context information
    rating.profil = profil
    add_karma_for_posting(rating)
    rating.menu = menu
    rating.save()
    
    # Add Karma
    add_karma_for_posting(rating, amount=1)
    
    return ("Success!", 0)


def add_karma_for_posting(post, amount=5):
    """
    add_karma_for_posting Gives the user Karma for posting a review, image or rating

    :param post: The Post object which contains the profil
    :type post: Image, Review or Rating
    :param amount: The amount of karma the user gets for posting, defaults to 5
    :type amount: int, optional
    """
    if post.profil:
        post.profil.karma += amount
        post.profil.save()

    return
