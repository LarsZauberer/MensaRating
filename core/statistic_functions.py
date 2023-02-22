from .models import MenuType, Menu, Rating, Image, Profil, Badge, Review
from django.db.models import Avg, Max
import logging

log = logging.getLogger("statistic_functions")


class HelperMenu:
    """
     Helper class to store values of the menus
    """
    rating = 0
    allTimeRating = 0

    def __init__(self, menu):
        """
        __init__ Helper class to store more values for the menus.

        :param menu: Menu object to store.
        :type menu: Menu
        """
        self.menu = menu
        log.warning(f"Helper Menu class is deprecated! Please zip all the information together")


def getRating(menu):
    """
    getRating Calculate the rating for a menu.

    :param menu: Menu to calculate the rating for.
    :type menu: Menu
    :return: Returns the rating for a menu.
    :rtype: float
    """
    # Get the ratings
    rating = Rating.objects.filter(menu=menu).aggregate(Avg("rating"))

    if rating["rating__avg"] == None:
        return 0
    else:
        return float('%.1f' % rating["rating__avg"])


def getRatingOfAllTime(menuType):
    """
    getRatingOfAllTime Calculates the average rating of all time for a menu.

    :param menu: Menu to calculate the average rating for.
    :type menu: Menu
    :return: Returns the average rating of all time for a menu.
    :rtype: float
    """
    # Find all menu occurencies
    menus = Menu.objects.filter(menuType=menuType)

    # Find all ratings for all the menu occurencies
    rating = Rating.objects.filter(menu__in=menus).aggregate(Avg("rating"))

    if rating["rating__avg"] == None:
        return 0
    else:
        return float('%.1f' % rating["rating__avg"])


def get_all_images_sorted(menuType):
    allmenus = Menu.objects.filter(menuType=menuType)
    images = Image.objects.filter(menu__in=allmenus).order_by("-likes")

    if len(images) == 0:
        return None
    else:
        return images


def get_all_reviews_sorted(menuType):
    allmenus = Menu.objects.filter(menuType=menuType)
        
    reviews = Review.objects.filter(menu__in=allmenus).order_by("-likes")

    if len(reviews) == 0:
        return None
    else:
        return reviews

def count_best_posts_of_profil(profil: Profil, best_post_function) -> int:
    # Count of most liked images
    menuTypes: list[MenuType] = MenuType.objects.all()
    counter: int = 0
    for i in menuTypes:
        if  best_post_function(i) != None:
            post = best_post_function(i)[0]
            if post.profil == profil:
                counter += 1
    
    return counter

def getNumRates(menu):
    return Rating.objects.filter(menu=menu).count()
    
def getNumRatesOfAllTime(menuType):
    menus = Menu.objects.filter(menuType=menuType)
    return Rating.objects.filter(menu__in=menus).count()

def get_badges_of_profil(profil: Profil):
    karma: int = profil.karma

    badges: list[Badge] = Badge.objects.all()
    
    img_counter: int = count_best_posts_of_profil(profil=profil, best_post_function=get_all_images_sorted)
    review_counter: int = count_best_posts_of_profil(profil=profil, best_post_function=get_all_reviews_sorted)
    categories: list[int] = [karma, img_counter, review_counter]
    
    # Get the highest badge for all the categories
    highest_badges: list[Badge] = [None for _ in categories]
    for i in badges:
        if i.count <= categories[i.condition_category]:  # Does the profil have this badge
            # Check if the badge is more worth than the saved.
            if highest_badges[i.condition_category] is None:
                highest_badges[i.condition_category] = i
            else:
                if highest_badges[i.condition_category].count < i.count:
                    highest_badges[i.condition_category] = i
    
    highest_badges = [i for i in highest_badges if i is not None]  # Remove all None
    
    return highest_badges
