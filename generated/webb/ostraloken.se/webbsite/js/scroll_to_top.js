const go_up_button_element = document.getElementById("go_up");

go_up_button_element.addEventListener("click", () => {
    document.documentElement.style.scrollBehavior = "smooth";
    setTimeout(() => { /*So that scrollbehavior has time to get set to smooth*/
        window.scrollTo(0, 0)
        document.documentElement.style.scrollBehavior = "auto";
    }, 10);
});

document.addEventListener("DOMContentLoaded", () => { check_if_show() });
document.addEventListener("scroll", () => { check_if_show() });

function check_if_show() {
    if (window.scrollY <= window.innerHeight) {
        go_up_button_element.classList.remove("show")
    } else {
        go_up_button_element.classList.add("show")
    };
};