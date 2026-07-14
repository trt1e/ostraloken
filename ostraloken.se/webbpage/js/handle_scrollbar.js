// ----------------------------------------------------------
// Scrollbar hidden is handled in handle_header.js
// ----------------------------------------------------------
const scrollbar_element = document.querySelector("#scrollbar");
const scrollbar_area_element = document.querySelector("#scrollbar_area");

document.addEventListener("DOMContentLoaded", () => { position_scrollbar() });
document.addEventListener("scroll", () => { position_scrollbar() });
document.addEventListener("resize", () => { position_scrollbar() });

function position_scrollbar() {
    // get where you are rn in the scroll
    const scroll_position = window.scrollY;
    // get the max scroll that you can scroll
    const scroll_limit = document.documentElement.offsetHeight - document.documentElement.clientHeight;

    // Set the scrollbar where it should be
    const wanted_scrollbar_position = (scroll_position / scroll_limit) * (document.documentElement.clientHeight - scrollbar_element.clientHeight);
    scrollbar_element.style.top = wanted_scrollbar_position + "px";

    // Set the scrollbars height right
    const wanted_scrollbar_height = (document.documentElement.clientHeight / scroll_limit) * 1000
    scrollbar_element.style.height = wanted_scrollbar_height + "px";
    console.log("Scrollbar height set to: " + wanted_scrollbar_height)
};

let move_mouse = false;
let last_mouse_pos = 0;

scrollbar_element.addEventListener("mousedown", () => { start_drag_scrollbar() });
scrollbar_area_element.addEventListener("mouseup", () => { stop_drag_scrollbar() });
scrollbar_area_element.addEventListener("mouseleave", () => { stop_drag_scrollbar() });

scrollbar_area_element.addEventListener("mousemove", (event) => { drag_scrollbar(event) });

function start_drag_scrollbar() {
    move_mouse = true;

    console.log("Started draging");
};
function stop_drag_scrollbar() {
    move_mouse = false;

    console.log("Stoped draging");
};
function drag_scrollbar(event) {
    if (move_mouse) {
        // get where you are rn in the scroll
        const scroll_position = window.scrollY;
        // get the max scroll that you can scroll
        const scroll_limit = document.documentElement.offsetHeight - document.documentElement.clientHeight;

        // get where the scrollbar is rn
        const scrollbar_element_currant_y_position = scrollbar_element.offsetTop;
        // get where the mouse is rn
        const mouse_y_position = event.clientY;

        // Set the position where it should be
        const wanted_y_position = ((mouse_y_position - last_mouse_pos) * (scroll_limit / document.documentElement.clientHeight)) + scroll_position;
        window.scrollTo(0, wanted_y_position);
    };
    last_mouse_pos = event.clientY;
};