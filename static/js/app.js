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
})