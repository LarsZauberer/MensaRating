from .models import MenuType, Menu, Rating, Image
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


def getMostLikedImage(menuType):
        allmenus = Menu.objects.filter(menuType=menuType)
        
        image = Image.objects.filter(menu__in=allmenus).order_by("-likes")

        if len(image) == 0:
            return None
        else:
            return image[0]





