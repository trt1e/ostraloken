/* ONLINE:
import * as pdfjs from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.mjs"; 
pdfjs.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.worker.mjs";
*/

import * as pdfjs from "./PDFjs/pdf.mjs";
pdfjs.GlobalWorkerOptions.workerSrc = "./pdf.worker.mjs";

const pdfContent = document.getElementById("main_pdf");
const pdfNumber = document.getElementById("pdf_upplaga_number");
const baseUrl = "\pdfs/";
const amoutPDfs = 40; // Change this when adding new upplagor

let numberOfPages;
let counter = amoutPDfs;
let renderMode = "browser"; // "browser" vs "JSrender"

window.addEventListener("load", () => {
    // get query info in the url (like ostraloken.se/pdfer/?upplaga=15)
    const queryString = window.location.search;
    const urlParameters = new URLSearchParams(queryString);
    // extract
    const wantedUpplagaNumber = urlParameters.get("upplaga")
    // if there is a upplaga request in url it sets it as the first 
    if (wantedUpplagaNumber) {
        counter = parseInt(wantedUpplagaNumber);
    };

    PDFHandle();
    pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
    console.log(pdfContent.src)
    if (window.innerWidth < 800) { // if window is this small, we can assume they are on phone or tablet
        console.log("Under 800 width: switching to JS render")
        switchImageFormat(); // If so, make it render in image rendering since webrendering ussualy doesn't work on phone or tablet
    };
});

function getLokenEdition(edition) {
    const loadingTask = baseUrl + "Östra_Löken_upplaga_" + edition + ".pdf";
    return loadingTask;
};

// when edition is selected, this renders out all the pages
async function renderDocument(pdfName) {
    const loadingTask = pdfjs.getDocument(pdfName);
    console.log("Loading: " + pdfName);

    const pdf = await loadingTask.promise; 
    numberOfPages = pdf.numPages;

    const containerElement = document.getElementById("pdf_container"); 

    // loop throught every page
    for (let page = 1; page <= numberOfPages; page++) {
        // create the canvas for the page
        const canvasElement = document.createElement("canvas");
        canvasElement.className = "pdf_page";
        canvasElement.id = "page_" + page;
        containerElement.appendChild(canvasElement);

        // fill the canvas with the right page of the pdf
        const canvases = document.getElementsByClassName("pdf_page");
        const canvas = canvases[page - 1];
        console.log("Loading page " + page);
        const canvas_context = canvas.getContext("2d");
        // get the page from pdf.js
        const pdf_page = await pdf.getPage(page);
        // set the viewport (like how high rez it is)
        const viewport = pdf_page.getViewport({ scale: 2.0 }); 
        canvas.width = viewport.width; 
        canvas.height = viewport.height;  
    
        pdf_page.render({ 
            canvasContext: canvas_context, 
            viewport: viewport,
        });    
    };
};

// unrender all the pages so renderDocument() works properly
async function unrenderDocument() {
    const canvasElement = document.getElementsByClassName("pdf_page");
        
    for (let page = 0; page <= numberOfPages - 1; page++) {
        canvasElement[0].remove();
        console.log("Removed page " + page + "s canvas");
    };
};

// back button
document.querySelector(".pdf_nav_buttons#previous").addEventListener("click", async () => {
    counter -= 1;
    if (counter < 1) {
        counter = amoutPDfs;
    };
    PDFHandle();
    if (renderMode == "browser") {
        pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
    } else {
        unrenderDocument();
        document.getElementById("pdf_loading_text").style.display = "block";
        await renderDocument(getLokenEdition(counter));
        document.getElementById("pdf_loading_text").style.display = "none";
    };
});

// byt bildform button
async function switchImageFormat() {
    if (renderMode == "browser") {
        renderMode = "JSrender";
        bildformText.innerText = "byt till browserrendering";
        document.getElementById("main_pdf").style.display = "none";
        document.getElementById("pdf_loading_text").style.display = "block";
        await renderDocument(getLokenEdition(counter));
        document.getElementById("pdf_loading_text").style.display = "none";
    } else {
        renderMode = "browser";
        bildformText.innerText = "byt till bildrendering";
        pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
        document.getElementById("main_pdf").style.display = "block";
        await unrenderDocument();
    };
    console.log("render mode now " + renderMode)
};
const bildformText = document.querySelector("#pdf_nav_switch_render p")
document.getElementById("pdf_nav_switch_render").addEventListener("click", async () => {
    await switchImageFormat();
});

// next button
document.querySelector(".pdf_nav_buttons#next").addEventListener("click", async () => {
    counter += 1;
    if (counter > amoutPDfs) {
        counter = 1;
    };
    PDFHandle();
    if (renderMode == "browser") {
        pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
    } else {
        unrenderDocument();
        document.getElementById("pdf_loading_text").style.display = "block";
        await renderDocument(getLokenEdition(counter));
        document.getElementById("pdf_loading_text").style.display = "none";
    };
});

function PDFHandle() {
    console.log(pdfContent);
    console.log(counter);
    pdfNumber.innerText = `Upplaga ${counter} / ${amoutPDfs}`;
};