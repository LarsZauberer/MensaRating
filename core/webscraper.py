# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import requests
import re
from .models import Menu, MenuType
import logging
import datetime as dt

log = logging.getLogger("Webscraper")

def get_menu_list(days):
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

def get_day_data():
    page = requests.get("https://neuekanti.sv-restaurant.ch/de/menuplan/")
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find_all(attrs={"class":"menu-plan-grid"})

def main():
    days = get_day_data()
    
    # Print
    for dishesOfDay in get_menu_list(days).values():
        for dish in dishesOfDay.values():
            for element in dish.values():
                print(element)
            print("")
    
    print(get_menu_list(days))

def webscrape():
    days = get_day_data()
    return get_menu_list(days)

def create_menu_in_database(title, description, label):
    menuType = MenuType.objects.filter(name=title)
    if len(menuType) == 0:
        log.info(f"No menuType with the name: {title} found.")
        menuType = [MenuType.objects.create(name=title)]
        log.info(f"Created menuType: {menuType[0]}")
    menuType = menuType[0]
    
    labels = [
        {"vegetarian": False, "vegan": False},
        {"vegetarian": True, "vegan": False},
        {"vegetarian": False, "vegan": True},
    ]
    
    Menu.objects.create(name=title, description=description, menuType=menuType, **labels[label])
    

def sync_today_menu():
    # Check if todays menu is already in database
    log.debug(f"Checking if todays menu is already in the database")
    menus = Menu.objects.filter(date=dt.date.today())
    
    # Retrieve mensa data
    log.debug(f"Retrieving mensa data")
    data = webscrape()
    log.debug(f"Data received: {data}")
    
    titles = [i.name for i in menus]
    for i in data["menu0"].keys():
        if data["menu0"][i]["title"] not in titles:
            log.info(f"Menu \"{data['menu0'][i]['title']}\" is not in the database")
            create_menu_in_database(data["menu0"][i]["title"], data["menu0"][i]["description"], data["menu0"][i]["label"])
            log.info(f"Created menu: {data['menu0'][i]['title']}")


if __name__ == "__main__":
    main()