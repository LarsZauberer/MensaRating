from .models import Menu, Rating


class HelperMenu:
    rating = 0
    allTimeRating = 0
    def __init__(self, menu):
        """
        __init__ Helper class to store more values for the menus.

        :param menu: Menu object to store.
        :type menu: Menu
        """
        self.menu = menu


def getRating(menu):
    """
    getRating Calculate the rating for a menu.

    :param menu: Menu to calculate the rating for.
    :type menu: Menu
    :return: Returns the rating for a menu.
    :rtype: float
    """
    # Get the ratings
    ratings = Rating.objects.filter(menu=menu)
    
    # Calculate the average rating for the menu today (not of all time)
    rates = []
    for i in ratings:
        rates.append(i.rating)
        
    if len(rates) == 0:
        return 0
        
    rating = sum(rates) / len(rates)
    return rating


def getRatingOfAllTime(menu):
    """
    getRatingOfAllTime Calculates the average rating of all time for a menu.
    
    :param menu: Menu to calculate the average rating for.
    :type menu: Menu
    :return: Returns the average rating of all time for a menu.
    :rtype: float
    """
    # Find all menu occurencies
    menus = Menu.objects.filter(name=menu.name)
    
    # Find all ratings for all the menu occurencies
    ratings = []
    for i in menus:
        ratings += Rating.objects.filter(menu=menu)
    
    # Calculate the average rating
    rates = []
    for i in ratings:
        rates.append(i.rating)
        
    if len(rates) == 0:
        return 0
    
    rating = sum(rates) / len(rates)
    return rating