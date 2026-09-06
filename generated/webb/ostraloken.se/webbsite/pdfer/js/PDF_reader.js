const pdfContent = document.querySelector("#main_pdf");
const pdfImgContainer = document.querySelector("#pdf_img_container");
const pdfNumber = document.querySelector("#pdf_utgava_number");
const baseFileUrl = "\pdf_files/";
const baseImagesUrl = "\pdf_images/";


// DO NOT TOUCH!!!
const maxPages = 5; // This specific variable is changed with engine/build/build_pdfs.py
const pagesPerPDF = [1, 2, 2, 2, 2, 3, 2, 2, 4, 2, 3, 3, 4, 3, 3, 4, 4, 3, 3, 4, 4, 2, 3, 3, 3, 2, 2, 3, 3, 4, 3, 4, 3, 3, 2, 4, 3, 2, 2, 3, 3, 5, 3] // This specific variable is changed with engine/build/generate_frontend.py
// DO NOT TOUCH!!!

const amoutPDFs = pagesPerPDF.length;

let numberOfPages;
let currant_utgava = amoutPDFs;
let renderMode = "image"; // "browser" vs "image", we start on image since it is faster and better for viewing

window.addEventListener("load", () => {
    // get query info in the url (like ostraloken.se/pdfer/?utgava=15)
    const queryString = window.location.search;
    const urlParameters = new URLSearchParams(queryString);
    // extract
    const wantedutgavaNumber = urlParameters.get("utgava")
    // if there is a utgava request in url it sets it as the first 
    if (wantedutgavaNumber) {
        currant_utgava = parseInt(wantedutgavaNumber);
    };

    // Load the right amount of image elements so that images can be placed inside them
    const containerElement = document.getElementById("pdf_img_container");  
    for (let image_element_number = 1; image_element_number <= maxPages; image_element_number++) {
        const imgElement = document.createElement("img");
        imgElement.className = "pdf_page";
        imgElement.id = "page_" + image_element_number;
        containerElement.appendChild(imgElement);
    };

    render();
});

// back button
document.querySelector(".pdf_nav_buttons#previous").addEventListener("click", async () => {
    currant_utgava -= 1;
    if (currant_utgava < 1) {
        currant_utgava = amoutPDFs;
    };
    render();
});

// byt bildform button
document.querySelector("#pdf_nav_switch_render").addEventListener("click", async () => {
    const bildformText = document.querySelector("#pdf_nav_switch_render p")
    if (renderMode == "browser") {
        renderMode = "image";
        bildformText.innerText = "byt till browserrendering";
    } else { // renderMode == "image"
        renderMode = "browser";
        bildformText.innerText = "byt till bildrendering";
    };
    render();
    console.log("Render mode now " + renderMode);
});

// next button
document.querySelector(".pdf_nav_buttons#next").addEventListener("click", async () => {
    currant_utgava += 1;
    if (currant_utgava > amoutPDFs) {
        currant_utgava = 1;
    };
    render();
});

function render() {
    const loadingText = document.querySelector("#pdf_loading_text");
    // Start render
    loadingText.style.display = "block";
    pdfNumber.style.display = "none";
    pdfImgContainer.style.display = "none";

    // Uppdate the text saying what utgava it is
    pdfNumber.innerText = `utgava ${currant_utgava} / ${amoutPDFs}`;

    // Render the utgava for browser view
    pdfContent.src = `./pdf_files/Ostra_Loken_utgava-${currant_utgava}.pdf`;
    if (renderMode == "browser") {
        pdfContent.style.display = "block"
    } else { // renderMode == "image"
        pdfContent.style.display = "none"
    };

    // Render the utgava for image view
    const howManyPages = pagesPerPDF[currant_utgava - 1] // How many pages this utgava has
    for (let page = 1; page <= maxPages; page++) { // go through all pages elements (even them with no image)
        const currantPageElement = document.querySelector(`.pdf_page#page_${page}`)

        // If renderMode is image and page is a image: renders
        if ((renderMode == "image") && (page <= howManyPages)) {
            currantPageElement.src = `./pdf_images/Utgava_${currant_utgava}/page_${page}.webp`;
            currantPageElement.style.display = "block";
        } else { // If renderMode is browser or page does not have a image
            currantPageElement.style.display = "none"; // Do not render
        };
    };

    // End render
    pdfNumber.style.display = "block";
    pdfImgContainer.style.display = "block";
    loadingText.style.display = "none";
    
    console.log("Renderd utgava " + currant_utgava)
};