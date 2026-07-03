function toggleMenu() {

    document
        .getElementById("navLinks")
        .classList
        .toggle("show-menu");

}

window.onclick = function (event) {

    let menu = document.getElementById("navLinks");

    let button = document.querySelector(".menu-toggle");

    if (
        !menu.contains(event.target)
        &&
        !button.contains(event.target)
    ) {

        menu.classList.remove("show-menu");

    }

}