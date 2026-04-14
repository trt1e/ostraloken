function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
};

function render_normal_storys() {
    const all_storys_json = httpGet("http://127.0.0.1:5000/normal_storys");
    const all_storys_parsed = JSON.parse(all_storys_json);
    console.log(all_storys_parsed.length);

    const main_object = document.querySelector("main")
    
    let upplagor_data = {}; // This is where the articles are in order

    for (let upplaga_number = 0; upplaga_number < all_storys_parsed.length; upplaga_number++) { // This is so js can order them
        const upplagor_object = all_storys_parsed[upplaga_number]; // this is just getting the object out
        upplagor_data[upplagor_object["Upplaga"]] = upplagor_object["Content"];
    };

    for (let upplaga_number = all_storys_parsed.length; upplaga_number >= 1; upplaga_number--) { // Same thing as erlyer only now orderd
        console.log(upplaga_number)
        for (let article_number = 0; article_number < upplagor_data[upplaga_number].length; article_number++) {
            const article_all_info = upplagor_data[upplaga_number][article_number];
            
            const article_title = article_all_info["Title"];
            const article_type = article_all_info["Type"];
            const article_writer = article_all_info["Writer"];
            const article_article = article_all_info["Article"];
            // The order is correct by default

            // create the a containing the article
            const article_container_element = document.createElement("a");
            article_container_element.href = "";
            article_container_element.className = "article";
            const article_container_element_in_main = main_object.appendChild(article_container_element);
            
            // add the image
            const article_img_element = document.createElement("img");
            article_img_element.src = "./images/Test.png";
            article_container_element_in_main.appendChild(article_img_element);
            
            // add the title
            const article_title_element = document.createElement("h2");
            article_title_element.textContent = article_title;
            if (article_title_element.textContent.length >= 60) {
                article_title_element.textContent = article_title.substring(0, 60) + "...";
            };
            article_container_element_in_main.appendChild(article_title_element);
            
            // add the text
            const article_text_element = document.createElement("p");
            article_text_element.textContent = article_article.substring(0, 120) + "...";
            article_container_element_in_main.appendChild(article_text_element);
        };
    };
};

render_normal_storys();