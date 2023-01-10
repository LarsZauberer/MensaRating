# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import requests
import re
# from datetime import datetime

page = requests.get("https://neuekanti.sv-restaurant.ch/de/menuplan/")
soup = BeautifulSoup(page.content, "html.parser")
days = soup.find_all(attrs={"class":"menu-plan-grid"})

def get_menu_list():
    menuListDict = {}

    for menuIndex, day in enumerate(days):
        dishesOfDayDict = {}
        dishes = day.find_all(attrs={"class":"menu-item"})
        
        for dishIndex, dish in enumerate(dishes):
            dishDict = {}

            # get title and description of dish with html tags as strings and using the "clean()" function to remove tags and double spaces
            title = clean(str(dish.find("h2")))
            description = clean(str(dish.find(attrs={"class":"menu-description"})))
            
            # find out if dish is served with meat (0), vegetarian (1) or vegan (2)
            if (dish.find(attrs={"class":"label label-vegetarian has-infobox"}) is not None):
                label = 1
            elif (dish.find(attrs={"class":"label label-vegan has-infobox"}) is not None):
                label = 2
            else:
                label = 0

            # add gathered information to current dish of the day in the list
            dishDict["title"] = title
            dishDict["description"] = description
            dishDict["label"] = label
            
            # add complete menu to the list
            dishesOfDayDict[f"dish{dishIndex}"] = dishDict

        
        # add all menus of the day to the list
        menuListDict[f"menu{menuIndex}"] = dishesOfDayDict
    
    # return list of every menu of every day
    return menuListDict

def clean(str):
    # uses regex to substitute tags and double spaces in messy html string with empty strings or single spaces
    string = re.sub('<p class="menu-description">|</p>|<h2 class="menu-title">|</h2>|<br/>\s|\\xad\s*|\\n', '', str)
    return string

def main():
    # Print
    for dishesOfDay in get_menu_list().values():
        for dish in dishesOfDay.values():
            for element in dish.values():
                print(element)
            print("")
    
    print(get_menu_list())


if __name__ == "__main__":
    main()