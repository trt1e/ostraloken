const header_element = document.querySelector("header");

let scroll_position = 0;
let old_scroll_position = 0;
let position_diffrance = 0;
let positive_counter = 0; // how long you have scrolled up
let negative_counter = 0; // how long you have scrolled down

document.addEventListener("scroll", () => {
    const scrollbar_element = document.querySelector("#scrollbar");
    
    scroll_position = window.scrollY;
    position_diffrance = scroll_position - old_scroll_position;
    if (position_diffrance > 0) {
        negative_counter += Math.abs(position_diffrance);
        positive_counter = 0;
    } else {
        positive_counter += Math.abs(position_diffrance);
        negative_counter = 0;
    };
    if (positive_counter >= 1) {
        header_element.classList.remove("header_hidden");
        // scrollbar_element.classList.add("scrollbar_hidden");
    } else if (negative_counter >= 80) {
        header_element.classList.add("header_hidden");
    };
    /*
    if (negative_counter >= 180) {
        scrollbar_element.classList.remove("scrollbar_hidden");
    };
    */

    old_scroll_position = scroll_position;
});