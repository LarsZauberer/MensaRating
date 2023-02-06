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

    removeAlertAfterDelay();
})

function removeAlertAfterDelay() {
    alerts = document.getElementsByClassName("alert");
    for (let index = 0; index < alerts.length; index++) {
        const element = alerts[index];
        setTimeout(closeAlert, 3000, element)
    }
}

function closeAlert(domElement) {
    domElement.style.display='none';
}
