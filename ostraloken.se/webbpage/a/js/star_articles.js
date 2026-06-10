const star_button_element = document.querySelector("button#star");
const star_filled_element = document.querySelector("button#star #star_filled");
const article_element = document.querySelector("article.article");

const article_id = article_element.id;
let star_status_storage = localStorage.getItem("star-status-" + article_id);
let star_status;

if (star_status_storage) {
    star_status = star_status_storage;
    console.log("Star status got from storage and is " + star_status)
} else {
    star_status_storage = localStorage.setItem("star-status-" + article_id, "empty");
    star_status = "empty"
    console.log("Star status set to " + star_status)
};

window.addEventListener("DOMContentLoaded", () => {
    check_star_status("filled"); // just check if it is stared at the start
    // the reason we use diffrent make_filled_when is since we first just want to check if the star should be filled, later however we want to change it
});

star_button_element.addEventListener("click", () => {
    check_star_status("empty"); // now we change it if the button is pressed
});

function check_star_status(make_filled_when) {
    if (star_status == make_filled_when) { // then make filled
        star_filled_element.style.opacity = "100%";
        star_status = "filled";
        star_status_storage = localStorage.setItem("star-status-" + article_id, "filled"); // save to local storage
        console.log("Star now filled");
    } else { // then make empty
        star_filled_element.style.opacity = "0%";
        star_status = "empty";
        star_status_storage = localStorage.setItem("star-status-" + article_id, "empty"); // save to local storage
        console.log("Star now empty");
    };
};

// star read also articles
const read_also_article_elements = document.querySelectorAll("#read_also .article");

window.addEventListener("DOMContentLoaded", () => {
    read_also_article_elements.forEach(article => {
        const article_id = article.id;

        let star_status_storage = localStorage.getItem("star-status-" + article_id);
        let star_status = "Empty";
        if (star_status_storage) {
            star_status = star_status_storage;
        };

        // make article highlighted if it is stared
        if (star_status == "filled") { // if filled
            // add highlight class to article
            article.classList.add("highlight")

            // show the star icon in the corner
            const star_icon = document.querySelector("#" + article_id + " .stared_article_icon");
            star_icon.style.display = "Block";
        };
    });
});