function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
};

function render_normal_storys() {
    const all_storys_json = httpGet("http://127.0.0.1:5000/normal_storys");
    const all_storys_parsed = JSON.parse(all_storys_json);
    console.log(all_storys_parsed);

    for (let story_number = 0; story_number < all_storys_parsed.length; story_number++) {
        const article_info_extracted = all_storys_parsed[story_number]["full_info_article_" + (story_number + 1)]

        const title = article_info_extracted["Title"];
        const type = article_info_extracted["Type"];
        const writer = article_info_extracted["Writer"];
        const story = article_info_extracted["Article"];
    };
};

render_normal_storys();