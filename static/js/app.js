//Navbar
//Warten bis DOM geladen ist
document.addEventListener("DOMContentLoaded", function (e) {
    const activePage = window.location.pathname;
    const navLinks = document.querySelectorAll("nav a")
    for (i = 0; i < navLinks.length; i++) {
        if (navLinks[i].toString().includes(activePage)) {
            var parentDiv = navLinks[i].parentElement;
            parentDiv.classList.add("active");
            return;
        }
    }
    update_all_btn();
    removeAlertAfterDelay();
})


function change_cursor_wait() {
    document.body.style.cursor = 'wait';
}

function update_all_btn() {
    likeButtons = document.getElementsByClassName("like-btn");
    for (let index = 0; index < likeButtons.length; index++) {
        const element = likeButtons[index];
        id = element.id.replace("-btn", "")
        post = localStorage.getItem(id + "-" + username);


        console.log(post);
        if (post) {
            element.className = element.className.replace(" disliked", "");
            element.className += " liked";
        } else {
            element.className = element.className.replace(" disliked", "");
            element.className += " disliked";
        }

        // if (element.classList.contains("liked")) {
        //     console.log("test");
        //     element.className = element.className.replace(" liked", "")
        //     element.className += " disliked"
        // } else {
        //     console.log("test1");
        //     element.className = element.className.replace(" disliked", "")
        //     element.className += " liked"
        // }

        // if (post) {
        //     element.innerHTML = "Dislike"
        //     if (!element.className.includes("disliked")) {
        //         element.className = element.className.replace(" liked", "")
        //         element.className += " disliked"
        //     }
        // } else {
        //     element.innerHTML = "Like"
        //     if (!element.className.includes("liked")) {
        //         element.className = element.className.replace(" disliked", "")
        //         element.className += " liked"
        //     }
        // }
    }
}


function like(cat, pk) {
    const post = localStorage.getItem(cat + "-" + pk + "-" + username);

    change_like = function () {
        console.log(this.responseText);
        if (this.status == 200) {
            document.getElementById(cat + "-" + pk).innerHTML = this.responseText
        }
    }

    if (post) {
        // Dislike
        api.get("like/" + cat + "/" + pk, "?dislike=YES", change_like);
        localStorage.removeItem(cat + "-" + pk + "-" + username);
        update_all_btn();
    } else {
        api.get("like/" + cat + "/" + pk, "", change_like);
        localStorage.setItem(cat + "-" + pk + "-" + username, "YES");
        update_all_btn();
    }
}

function removeAlertAfterDelay() {
    alerts = document.getElementsByClassName("alert");
    for (let index = 0; index < alerts.length; index++) {
        const element = alerts[index];
        setTimeout(closeAlert, 3000, element)
    }
}


function closeAlert(domElement) {
    domElement.style.display = 'none';
}

function togglePopup() {
    popup = document.getElementById("popup");
    if (popup.style.display == "none") {
        popup.style.display = "flex"
    }
    else {
        popup.style.display = "none"
    }
}

//Zeigt Pop Up um Profil Bild zu ändern
function showPopUp() {
    console.log("test");
    document.getElementById("popUp").style.display = "block";
}

//lässt Pop Up um Profil Bild zu ändern verschwinden
function hidePopUp() {
    console.log("test2");
    document.getElementById("popUp").style.display = "none";
}