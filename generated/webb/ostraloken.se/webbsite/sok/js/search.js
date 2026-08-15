const query_string = window.location.search;
const search_bar_element = document.querySelector("#search_bar");
const all_article_elements = document.querySelectorAll(".article");
const feed_element = document.querySelector("#feed");
const loading_element = document.querySelector("#loading_text");
const empty_element = document.querySelector("#empty_text");

const url_params = new URLSearchParams(query_string);
const org_static_elements_array = Array.from(all_article_elements); // use this so we dont change the DOM

window.addEventListener("DOMContentLoaded", () => {
    // if there is a search term in the url, we search it
    const url_input = url_params.get("s");
    if (url_params.has("s")) {
        search_bar_element.value = url_input;
        search(url_input);
    };
});

search_bar_element.addEventListener("input", () => {
    const search_input = search_bar_element.value;
    console.log("User wrote: " + search_input);
    search(search_input);
});

function search(input) {
    if (input.length >= 2) {
        feed_element.style.display = "None";
        loading_element.style.display = "Block";
        const static_elements_array = Array.from(all_article_elements); // use this so we dont change the DOM
        const fixed_search_input = input.toLowerCase();
        let no_articles = true;
        all_article_strings = [];
        article_order = [];
        static_elements_array.forEach(article => {
            const currant_article_string = String(article.innerText).toLowerCase();
            if (currant_article_string.search(fixed_search_input) != -1) {
                article.style.display = "Block";
                amount_of_search_match = (currant_article_string.match(new RegExp(fixed_search_input, "g")) || []).length; // how many times does the search word come up in the article

                article_package = {"amount_of_input": amount_of_search_match, "article": currant_article_string};
                article_order.push(article_package);
                no_articles = false;
            } else {
               article.style.display = "None";
            };
            all_article_strings.push(currant_article_string);
        });
        const article_order_sorted = article_order.sort((a, b) => (a.amount_of_input - b.amount_of_input)); // order the articles by the number they were given of how often the search term came up
        const article_order_sorted_reversed = article_order_sorted.reverse(); // reverse it so it is right
        article_order_sorted_reversed.forEach(article => {
            const currant_article = article.article;

            // place it at the top of the feed and since article_order_sorted is sorted, it automaticly adds them in the right order
            const article_element = static_elements_array[all_article_strings.indexOf(currant_article)];
            feed_element.appendChild(article_element);
        });
        
        feed_element.style.display = "Block";
        loading_element.style.display = "None";

        if (no_articles == true) {
            empty_element.style.display = "Block";
        } else {
            empty_element.style.display = "None";
        };

    } else {
        org_static_elements_array.forEach(article => {
            article.style.display = "Block";
            feed_element.appendChild(article);
        });
    };

    // add currant search to url
    url_params.set("s", input);
    history.replaceState(null, null, "?" + url_params.toString()); // uppdate url bar
};