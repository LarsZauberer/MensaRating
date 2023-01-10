# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime

def getMenuList():
    menus = []
    descriptions = []
    cleanMenus = []
    cleanDescriptions = []
    weekday = datetime.weekday(datetime.now())

    page = requests.get("https://neuekanti.sv-restaurant.ch/de/menuplan/")
    soup = BeautifulSoup(page.content, "html.parser")

    # get essential html data from webpage
    for n in range (1, 6):
        if n < weekday:
            tab = None
        else:
            tab = soup.find("div", attrs={"id":f"menu-plan-tab{n - weekday}"})
        
        if (tab != None):
            # menusOfDay = tab.find_all(attrs={"class":"item-content"})
            menuNameOfDay = tab.find_all("h2", attrs={"class":"menu-title"}) # gets every h2 title of class "menu-title"
            descriptionsOfDay = tab.find_all("p", attrs={"class":"menu-description"}) # gets all text of class "menu-description"
            # label = menusOfDay
            menus.append(menuNameOfDay)
            descriptions.append(descriptionsOfDay)
        else:
            menus.append(["empty", "empty"])
            descriptions.append(["empty", "empty"])

    # clean up messy html list of menu titles
    for day in menus:
        cleanDayMenus = []
        for menu in day:
            cleanText = re.sub('<h2 class="menu-title">|</h2>|<br/>|\\xad', '', str(menu))
            cleanText = re.sub('\\n|\s{2}',  ' ', cleanText)
            cleanDayMenus.append(cleanText)
        cleanMenus.append(cleanDayMenus)

    # clean up messy html list of descriptions
    for day in descriptions:
        cleanDayDescriptions = []
        for description in day:
            cleanText = re.sub('<p class="menu-description">|</p>', '', str(description))
            cleanDayDescriptions.append(cleanText)
        cleanDescriptions.append(cleanDayDescriptions)
    
    # combining menu titles with menu descriptions in one 3d array
    menusWithDescription = []
    for i in range (len(cleanMenus)):
        dayMenus = []
        for j in range (len(cleanMenus[i])):
            dayMenus.append([cleanMenus[i][j], cleanDescriptions[i][j]])
        menusWithDescription.append(dayMenus)
    
    return menusWithDescription


if __name__ == "__main__":
    for day in getMenuList():
        for menu in day:
            for part in menu:
                print(part)
            print("")
        print("\n")