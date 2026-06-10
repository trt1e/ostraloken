const star_button_element = document.querySelector("button#star");
const star_filled_element = document.querySelector("button#star #star_filled");
const all_article_elements = document.querySelectorAll("a.article");

window.addEventListener("DOMContentLoaded", () => {
    all_article_elements.forEach(article => {
        const article_id = article.id;

        let star_status_storage = localStorage.getItem("star-status-" + article_id);
        let star_status;

        if (star_status_storage) {
            star_status = star_status_storage;
        } else {
            star_status_storage = localStorage.setItem("star-status-" + article_id, "empty");
            star_status = "empty"
        };
        
        // make article highlighted if it is stared
        if (star_status == "filled") { // if filled
            article.classList.add("highlight")
        };
    });
});