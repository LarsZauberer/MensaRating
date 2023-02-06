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
})

function update_all_btn() {
    likeButtons = document.getElementsByClassName("like-btn")
    for (let index = 0; index < likeButtons.length; index++) {
        const element = likeButtons[index];
        id = element.id.replace("-btn", "")
        post = localStorage.getItem(id);
        if (post) {
            element.innerHTML = "Dislike"
            if (!element.className.includes("disliked")) {
                element.className = element.className.replace(" liked", "")
                element.className += " disliked"
            }
        } else {
            if (!element.className.includes("liked")) {
                element.innerHTML = "Like"
                element.className = element.className.replace(" disliked", "")
                element.className += " liked"
            }
        }
    }
}

function like(cat, pk) {
    const post = localStorage.getItem(cat + "-" + pk);

    change_like = function() {
        console.log(this.responseText);
        if (this.status == 200) {
            document.getElementById(cat + "-" + pk).innerHTML = this.responseText
        }
    }

    if (post) {
        // Dislike
        api.get("like/" + cat + "/" + pk, "?dislike=YES", change_like);
        localStorage.removeItem(cat + "-" + pk);
        update_all_btn();
    } else {
        api.get("like/" + cat + "/" + pk, "", change_like);
        localStorage.setItem(cat + "-" + pk, "YES");
        update_all_btn();
    }
}
