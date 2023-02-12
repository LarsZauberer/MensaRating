function orderMenutypes(menuTypes){
    menuTypes.sort(function(a, b){
        let x = a.occurrences;
        let y = b.occurrences;

        if(x < y) return 1;
        else if(x > y) return -1;
        return 0;


    })

    for(let i = 0; i < menuTypes.length; i++){
        let menuTypeObject = document.getElementById("menutype-" + i);
        let menuType = menuTypes[i]

        menuTypeObject.setAttribute("onclick", "location.href='" + menuType.url + "';")
       

        menuTypeObject = menuTypeObject.children

        menuTypeObject[0].innerHTML = menuType.name

        let vegivegan = menuTypeObject[1].children;
        if(menuType.vegetarian == "True"){
            vegivegan[0].style.width = "100%";
            vegivegan[0].style.height = "100%";
            vegivegan[0].style.opacity = "1";
        }else if(menuType.vegan == "True"){
            vegivegan[1].style.width = "100%";
            vegivegan[1].style.height = "100%";
            vegivegan[1].style.opacity = "1";
        }

        menuTypeObject[2].innerHTML = "Vorkommen: " + menuType.occurrences

        
    
        rating = menuTypeObject[3].children
        rating[0].innerHTML = menuType.rating
        starRate(i, menuType.rating)
        rating[2].innerHTML = "(" + menuType.numrates + ")"
    }
}