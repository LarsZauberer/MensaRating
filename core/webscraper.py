# Maintained: Valentin (Scraping), Ian (Database Synchronization)
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup  # To parse the html and analyze the data
import requests  # To make a HTTP Request to the mensa page
import re  # To use regex to scan the data
from .models import Menu, MenuType  # To have access to the database
import logging  # To gain logging information
import datetime as dt  # To save information about the date

log = logging.getLogger("Webscraper")

BLACKLIST = [
    "Ferien",
    "Kollegiumstag"
]

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
    string = re.sub('<p class="menu-description">|</p>|<h2 class="menu-title">|</h2>|\\xad\s*|\\n', '', str)
    string = string.replace("<br/>", " ")
    return string.strip()

def get_day_data():
    page = requests.get("https://neuekanti.sv-restaurant.ch/de/menuplan/")
    soup = BeautifulSoup(page.content, "html.parser")
    return soup.find_all(attrs={"class":"menu-plan-grid"})

def get_dates():
    page = requests.get("https://neuekanti.sv-restaurant.ch/de/menuplan/")
    soup = BeautifulSoup(page.content, "html.parser")
    day_nav = soup.find_all(attrs={"class": "day-nav"})[0]
    dates = day_nav.find_all(attrs={"class": "date"})
    
    for i, el in enumerate(dates):
        date = dt.datetime.strptime(el.contents[0], "%d.%m.").date()
        date_td = dt.date.today()
        date = date.replace(year=date_td.year)
        # check if this date is already happend -> Can happen at the end of the year
        # check if the date is more than 7 days in the past, so that this won't be triggered when the mensa page is not updated correctly.
        if date < date_td and date_td - date > dt.timedelta(days=7):
            date = date.replace(year=date_td.year + 1) # set it to next year
        dates[i] = date
    
    return dates

def main():
    days = get_day_data()
    get_dates()
    
    # Print
    for dishesOfDay in get_menu_list(days).values():
        for dish in dishesOfDay.values():
            for element in dish.values():
                print(element)
            print("")
    
    print(get_menu_list(days))

def webscrape():
    days = get_day_data()  # Get all the days
    dates = get_dates()  # Get the dates of the days
    return get_menu_list(days), dates  # Retrive all the information

def get_menu_type(title: str) -> MenuType:
    # Check if the menuType already exists
    menuType = MenuType.objects.filter(name=title)
    if len(menuType) == 0:
        # Create a new menuType
        log.info(f"No menuType with the name: {title} found.")
        try:
            menuType = [MenuType.objects.create(name=title)]
        except Exception as e:
            log.critical(f"Duplicate menuType")
            log.critical(f"Debug information: title: {title}, description: {description}, label: {label}, date: {date}, menuType: {menuType}")
            return
        log.info(f"Created menuType: {menuType[0]}")
    return menuType[0]

def create_menu_in_database(title, description, label, date):
    menuType = get_menu_type(title)
    
    # Create the menu
    # Create the labels
    labels = [
        {"vegetarian": False, "vegan": False},
        {"vegetarian": True, "vegan": False},
        {"vegetarian": False, "vegan": True},
    ]
    
    Menu.objects.create(name=title, description=description, menuType=menuType, date=date, **labels[label])

def update_menu_in_database(title, description, label, date, menu):
    menuType = get_menu_type(title)
    
    # Update the menu
    # Create the labels
    labels = [
        {"vegetarian": False, "vegan": False},
        {"vegetarian": True, "vegan": False},
        {"vegetarian": False, "vegan": True},
    ]
    
    menu.name = title
    menu.description = description
    menu.menuType = menuType
    menu.date = date
    menu.vegetarian = labels[label]["vegetarian"]
    menu.vegan = labels[label]["vegan"]
    menu.save()
    

def sync_today_menu():
    log.debug(f"Retrieving mensa data")
    data, dates = webscrape()
    log.debug(f"Data received: {data}, {dates}")

    for key, date in zip(data.keys(), dates):
        menus = Menu.objects.filter(date=date)
        
        # Update the menus with the new data
        # If the menu is not in the database, create it
        # If the menu is in the database, update it
        # If the menu is not in the new data, delete it
        
        for index, item in enumerate(data[key].keys()):
            # Blacklist menus
            if data[key][item]['title'] in BLACKLIST:
                continue
            
            # Check if the menu is in the database
            try:
                menu = menus[index]
                log.debug(f"Menu \"{data[key][item]['title']}\" already in database (DB: {menu})")
                update_menu_in_database(data[key][item]["title"], data[key][item]["description"], data[key][item]["label"], date, menu)  # Update the menu
                log.debug(f"Updated menu: {menu}")
            except IndexError:
                # Menu is not in the database -> create one
                log.info(f"Menu \"{data[key][item]['title']}\" is not in the database")
                create_menu_in_database(data[key][item]["title"], data[key][item]["description"], data[key][item]["label"], date)  # Create the menu
                log.info(f"Created menu: {data[key][item]['title']}")
        
        # Cleanup
        # Delete menuTypes that have 0 occurences
        allMenuTypes = MenuType.objects.all()
        for i in allMenuTypes:
            if len(Menu.objects.filter(menuType=i)) == 0:
                log.info(f"Deleting menuType: {i}")
                i.delete()
                continue


if __name__ == "__main__":
    main()