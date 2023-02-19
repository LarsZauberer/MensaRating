function i_orderMenutypes(orderType){
    if(orderType == "occ"){
        menuTypes.sort(function(a, b){
            let x = a.occurrences;
            let y = b.occurrences;

            if(x < y) return 1;
            else if(x > y) return -1;
            return 0;
        })
    }
    else if(orderType == "rating"){
        menuTypes.sort(function(a, b){
            let x = a.rating;
            let y = b.rating;

            if(x < y) return 1;
            else if(x > y) return -1;
            return 0;
        })
    }
    else if(orderType == "numrates"){
        menuTypes.sort(function(a, b){
            let x = parseInt(a.numrates);
            let y = parseInt(b.numrates);

            if(x < y) return 1;
            else if(x > y) return -1;
            return 0;
        })
    }

    i_updateListboxs(menuTypes)
    i_toggleStatOptions(1)
}

function i_filterMenutypes(filterType){
    for(let i = 0; i < menuTypes.length; i++){
        let menuType = menuTypes[i]

        if(filterType == "vegan"){
            if(menuType.vegan == "True") menuType.visible = true;
            else menuType.visible = false;
        }else if(filterType == "vegi"){
            if(menuType.vegetarian == "True") menuType.visible = true;
            else menuType.visible = false
        }
        else{
            menuTypes[i].visible = true
        }
    }
    
    i_updateListboxs()
    i_toggleStatOptions(0)
}
    
    


function i_updateListboxs(){
    for(let i = 0; i < menuTypes.length; i++){
        let menuTypeObject = document.getElementById("menutype-" + i);
        let menuType = menuTypes[i]
        
        menuTypeObject.style.display = "flex"
        if(!menuType.visible){
            menuTypeObject.style.display = "None"
        } 
        else{
            menuTypeObject.setAttribute("onclick", "location.href='" + menuType.url + "';")
            menuTypeObject = menuTypeObject.children
            menuTypeObject[0].innerHTML = menuType.name
            let vegivegan = menuTypeObject[1].children;

            vegivegan[0].style.width = vegivegan[0].style.height = "0";
            vegivegan[1].style.width =  vegivegan[1].style.height = "0";
            if(menuType.vegetarian == "True"){
                vegivegan[0].style.width = vegivegan[0].style.height = "100%";
            }else if(menuType.vegan == "True"){
                vegivegan[1].style.width =  vegivegan[1].style.height = "100%";
            }


            
        
            rating = menuTypeObject[2].children
            rating[0].innerHTML = menuType.rating
            starRate(i, menuType.rating)
            rating[2].innerHTML = "(" + menuType.numrates + ")"
        }    
    }
}




function i_toggleStatOptions(type) {
    let orderoptions = document.getElementsByClassName("stat-criteria")[type]
    let orderButtons = orderoptions.children

    if (orderoptions.style.height == "" || orderoptions.style.height == "0em") {
        orderoptions.style.height = "1em"
        for (let i = 0; i < orderButtons.length; i++) {
            orderButtons[i].style.height = "2em"
            orderButtons[i].style.opacity = 1;
            
        }
    }
    else {
        orderoptions.style.height = "0em"
        for (let i = 0; i < orderButtons.length; i++) {
            orderButtons[i].style.height = "0em"
            orderButtons[i].style.opacity = 0

        }
    }
}