//Maintained by Robin, Valentin
//This File handles the filter/sorting of the menutypes on the allMenu.html page

//different order options. Data gets saved in menuTypes array
function orderMenutypes(orderType) {
    if (orderType == "occ") {
        menuTypes.sort(function (a, b) {
            let x = a.occurrences;
            let y = b.occurrences;
            //descending order
            if (x < y) return 1;
            else if (x > y) return -1;
            return 0;
        })
    }
    else if (orderType == "rating") {
        menuTypes.sort(function (a, b) {
            let x = a.rating;
            let y = b.rating;
            //descending order
            if (x < y) return 1;
            else if (x > y) return -1;
            return 0;
        })
    }
    else if (orderType == "numrates") {
        menuTypes.sort(function (a, b) {
            let x = parseInt(a.numrates);
            let y = parseInt(b.numrates);
            //descending order
            if (x < y) return 1;
            else if (x > y) return -1;
            return 0;
        })
    }
    else if (orderType == "name") {
        menuTypes.sort(function (a, b) {
            return a.name.localeCompare(b.name); // alphabetical order
        })
    }
    updateListboxs()
    toggleStatOptions(1)
}

//different filter options. Data gets saved in menuTypes array
function filterMenutypes(filterType) {
    for (let i = 0; i < menuTypes.length; i++) {
        let menuType = menuTypes[i]
        //set visibility attribute of each menuType according to filter
        if (filterType == "vegan") {
            if (menuType.vegan == "True") menuType.visible = true;
            else menuType.visible = false;
        } else if (filterType == "vegi") {
            if (menuType.vegetarian == "True") menuType.visible = true;
            else menuType.visible = false
        }
        else {
            menuTypes[i].visible = true
        }
    }
    //update menus according to options
    updateListboxs()
    toggleStatOptions(0)
}

//update the html of the listboxes with the sorted/filter data in the menuTypes array
function updateListboxs() {
    for (let i = 0; i < menuTypes.length; i++) {
        let menuTypeObject = document.getElementById("menutype-" + i);
        let menuType = menuTypes[i]

        //make menutypes width visible == false invisible
        menuTypeObject.style.display = "flex"
        if (!menuType.visible) {
            menuTypeObject.style.display = "None"
        }
        else {
            menuTypeObject.setAttribute("onclick", "location.href='" + menuType.url + "';") //assign correct link to menu
            menuTypeObject = menuTypeObject.children
            menuTypeObject[0].innerHTML = menuType.name //first div == name
            
            let vegivegan = menuTypeObject[1].children;

            if (menuType.vegan == "True") {
                vegivegan[1].style.display = "block"; //show vegan label
                vegivegan[0].style.display = "none"; //don't show vegetarian label
            } else if (menuType.vegetarian == "True") {
                vegivegan[0].style.display = "block"; //show vegetarian label
                vegivegan[1].style.display = "none"; //don't show vegan label
            } else {
                vegivegan[0].style.display = "none"; //don't show vegetarian label
                vegivegan[0].style.display = "none"; //don't show vegan label
            }

            menuTypeObject[2].innerHTML = "Vorkommen: " + menuType.occurrences //show occurrences

            //update Rating
            rating = menuTypeObject[3].children
            rating[0].innerHTML = menuType.rating
            starRate(i, menuType.rating)
            rating[2].innerHTML = "(" + menuType.numrates + ")"
        }
    }
}

//Toggles visibility of the Options for filter/sorting
//Argument type (int): 0 -> targets filter button, 1 -> targets sort button
function toggleStatOptions(type) {
    let orderoptions = document.getElementsByClassName("stat-criteria")[type]
    let orderButtons = orderoptions.children

    if (orderoptions.style.height == "" || orderoptions.style.height == "0em") { //if not visible
        orderoptions.style.height = "1em"
        for (let i = 0; i < orderButtons.length; i++) { //Make every option visible
            orderButtons[i].style.height = "2em"
            orderButtons[i].style.opacity = 1;
        }
    }
    else { //currently visible
        orderoptions.style.height = "0em"
        for (let i = 0; i < orderButtons.length; i++) { //make every option invisible
            orderButtons[i].style.height = "0em"
            orderButtons[i].style.opacity = 0
        }
    }
}