const star_button_element = document.querySelector("button#star");
const star_filled_element = document.querySelector("button#star #star_filled");

let star_status_storage = localStorage.getItem("star-status");
let star_status;
star_status_storage = "";

if (star_status_storage) {
    star_status = JSON.parse(star_status_storage);
} else {
    star_status_storage = localStorage.setItem("star-status", "Empty");
    star_status = "Empty"
};

star_button_element.addEventListener("click", () => {
    if (star_status == "Empty") { // then make filled
        star_filled_element.style.opacity = "100%";
        star_status = "Filled";
    } else { // then make empty
        star_filled_element.style.opacity = "0%";
        star_status = "Empty";
    };
});