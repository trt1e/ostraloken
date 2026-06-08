const search_bar_element = document.querySelector("#search_bar");
const all_article_elements = document.querySelectorAll(".article");
const feed_element = document.querySelector("#feed");
const loading_element = document.querySelector("#loading_text");
const empty_element = document.querySelector("#empty_text");

const org_static_elements_array = Array.from(all_article_elements); // use this so we dont change the DOM

search_bar_element.addEventListener("input", () => {
    const search_input = search_bar_element.value;
    console.log("User wrote: " + search_input);

    if (search_input.length >= 2) {
        feed_element.style.display = "None";
        loading_element.style.display = "Block";
        const static_elements_array = Array.from(all_article_elements); // use this so we dont change the DOM
        const fixed_search_input = search_input.toLowerCase();
        const all_article_strings = [];
        let article_order = [];
        let no_articles = true;
        static_elements_array.forEach(article => {
            const currant_article_string = String(article.innerText).toLowerCase();
            if (currant_article_string.search(fixed_search_input) != -1) {
                article.style.display = "Block";
                amount_of_search_match = (currant_article_string.match(new RegExp(fixed_search_input, "g")) || []).length; // how many times does the search word come up in the article
                article_package = {"position": amount_of_search_match, "article": currant_article_string};
                article_order.push(article_package);
                no_articles = false;
            } else {
               article.style.display = "None";
            };
            all_article_strings.push(currant_article_string);
        });
        const article_order_sorted = article_order.sort((a, b) => (a.position - b.position)); // order the articles by the number they were given of how often the search term came up
        const article_order_sorted_reversed = article_order_sorted.reverse();
        article_order_sorted_reversed.forEach(article => {
            const currant_article = article.article;
            feed_element.appendChild(static_elements_array[all_article_strings.indexOf(currant_article)]);
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
});