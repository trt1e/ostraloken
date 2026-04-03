function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
};

function render_normal_storys() {
    const all_storys_json = httpGet("http://127.0.0.1:5000/normal_storys");
    const all_storys_parsed = JSON.parse(all_storys_json);
    // console.log(all_storys_parsed);

    const main_object = document.querySelector("main")

    let upplaga_adjusted = 0;
    for (let upplaga_number = 0; upplaga_number < all_storys_parsed.length; upplaga_number++) { 
        upplaga_adjusted = upplaga_number + 31; // change when having lower base upplaga
        const upplagor_object = all_storys_parsed[upplaga_number]; // this is just getting the object out
        const upplagor_data = upplagor_object[upplaga_adjusted]; // This is the arrey

        for (let article_number = 0; article_number < upplagor_data.length; article_number++) {
            const article_all_info = upplagor_data[article_number];
            
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