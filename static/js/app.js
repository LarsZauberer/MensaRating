// Maintained by: Ian, Robin

//Navbar
//Warten bis DOM geladen ist
document.addEventListener("DOMContentLoaded", function (e) {
    // Aktive Seite hervorheben
    const activePage = window.location.pathname;
    const navLinks = document.querySelectorAll("nav a")
    for (i = 0; i < navLinks.length; i++) {
        if (navLinks[i].toString().includes(activePage)) {
            var parentDiv = navLinks[i].parentElement;
            parentDiv.classList.add("active");
            return;
        }
    }
    update_all_btn();  // Update all the like buttons on the page if the user has already liked a post
    removeAlertAfterDelay();  // Remove the alert information after 3 seconds.
})

//Mobile Menu
function toggleMobileMenu() {
    console.log("test");
    const header = document.querySelectorAll("header");
    const navContainer = document.querySelectorAll("nav");
    const menuOpener = document.getElementById("mobileMenuOpener");
    const menuCloser = document.getElementById("mobileMenuCloser");
    
    if(navContainer[0].classList.contains("closeMenu")){
        // Menü anzeigen
        navContainer[0].classList.remove("closeMenu");
        header[0].classList.remove("allBorder");
        // Icon ändern
        menuOpener.classList.add("closeMenu");
        menuCloser.classList.remove("closeMenu");
        
    }else{
        // Menü verschwinden lassen
        navContainer[0].classList.add("closeMenu");
        header[0].classList.add("allBorder");
        // Icon ändern
        menuCloser.classList.add("closeMenu");
        menuOpener.classList.remove("closeMenu");
    }
}


// Change the cursor to a wait cursor
function change_cursor_wait() {
    document.body.style.cursor = 'wait';
}


// Update all the like buttons on the page if the user has already liked a post
function update_all_btn() {
    // Get all the like buttons
    likeButtons = document.getElementsByClassName("like-btn");
    for (let index = 0; index < likeButtons.length; index++) {

        // Get the id of the post and look up the information in the localstorage
        const element = likeButtons[index];
        id = element.id.replace("-btn", "")
        post = localStorage.getItem(id + "-" + username);


        // console.log(post);
        // If the post information exists -> user liked -> change the button state to liked
        element.className = element.className.replace(" disliked", "");
        element.className = element.className.replace(" liked", "");
        if (post) {
            element.className += " liked";
        } else {
            element.className += " disliked";
        }
    }
}


function like(cat, pk) {
    // Get the information of the post from the localstorage
    const post = localStorage.getItem(cat + "-" + pk + "-" + username);

    // Change the like button state after the request to the backend
    change_like = function () {
        console.log(this.responseText);
        if (this.status == 200) {
            document.getElementById(cat + "-" + pk).innerHTML = this.responseText
        }
    }

    if (post) {
        // Dislike
        api.get("like/" + cat + "/" + pk, "?dislike=YES", change_like);  // send to backend
        localStorage.removeItem(cat + "-" + pk + "-" + username);  // remove from localstorage
        update_all_btn();  // update the like buttons
    } else {
        // Like
        api.get("like/" + cat + "/" + pk, "", change_like);
        localStorage.setItem(cat + "-" + pk + "-" + username, "YES");
        update_all_btn();
    }
}

function removeAlertAfterDelay() {
    // for each alert remove it after 3 seconds
    alerts = document.getElementsByClassName("alert");
    for (let index = 0; index < alerts.length; index++) {
        const element = alerts[index];
        setTimeout(closeAlert, 3000, element)
    }
}


function closeAlert(domElement) {
    // Remove the alert
    domElement.style.display = 'none';
}

// Toggle the upload popup
function togglePopup(popup_id){
    popup = document.getElementById(popup_id);
    
    if (popup.style.display == "none") {
        popup.style.display = "flex";
    }
    else if (popup.style.display == "flex") {
        popup.style.display = "none";
    }
}

//calculate the number of the rating into a percentage of the yellow bar representing the stars
function starRate(index, rating) {
    let star = document.getElementById("stars-" + index);

    //convert rating number into string of percentage
    rating = +(rating.replace(",", "."))//convert string-number into float
    rating = String(rating / 5 * 100) + "%"//convert float to percentage-string

    star.style.width = rating
}

//Display of stars when hovering over them (in the case of giving a rating)
function starHover(stars, i) {
    for (let j = 0; j <= i; j++) {
        stars[j].style.backgroundImage = "url('../../static/images/yellowstar.png')"
    }
}
//Revert display when hovering ends
function stopStarHover() {
    for (let j = 0; j < 5; j++) {
        stars[j].style.backgroundImage = "url('../../static/images/emptystar.png')"
    }
}
