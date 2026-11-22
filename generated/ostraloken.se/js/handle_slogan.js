
document.addEventListener("DOMContentLoaded", () => {
    const slogan_element = document.querySelector("header #slogan");
    const type_text_elements = document.querySelectorAll("article .type_text");
    const type_text = type_text_elements[0];
    const file_name = document.title.split(" | ")[0];

    let set_slogan_to = "";

    if (type_text_elements.length == 1) {
        let text = type_text.innerText
        if (text.length > 15) {
            text = text.substring(0, 12) + "...";
        };
        set_slogan_to = "Hotfullt nära " + text.toLowerCase().replace("östra", "Östra");
    } else if (file_name != "Östra Löken") {
        let text = file_name
        if (text.length > 15) {
            text = text.substring(0, 12) + "...";
        };
        set_slogan_to = "Hotfullt nära " + text.toLowerCase().replace("östra", "Östra");
    } else {
        set_slogan_to = "Hotfullt nära verkligheten";
    };

    slogan_element.innerText = set_slogan_to;
    console.log("Slogan set to: " + set_slogan_to);
});
    