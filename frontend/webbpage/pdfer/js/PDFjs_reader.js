/* ONLINE:
import * as pdfjs from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.mjs"; 
pdfjs.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.10.38/pdf.worker.mjs";
*/

import * as pdfjs from "./PDFjs/pdf.mjs";
pdfjs.GlobalWorkerOptions.workerSrc = "./pdf.worker.mjs";

const pdfContent = document.getElementById("main_pdf");
const pdfNumber = document.getElementById("pdf_upplaga_number");
const baseUrl = "\pdfs/";
const amoutPDfs = 36; // Change this when adding new upplagor

let numberOfPages;
let counter = amoutPDfs;
let renderMode = "browser"; // "browser" vs "JSrender"

window.addEventListener("load", () => {
    PDFHandle();
    pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
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
document.getElementsByClassName("pdf_nav_buttons")[0].addEventListener("click", async () => {
    counter -= 1;
    if (counter < 1) {
        counter = amoutPDfs;
    };
    PDFHandle();
    if (renderMode == "browser") {
        pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
    } else {
        let backgroundColorBlob = document.getElementsByClassName("background_colorblob"); 
        for (let element = 0; element < backgroundColorBlob.length; element++) {
            let elementBlob = backgroundColorBlob[element];
            elementBlob.style.transition = "0s";
        };
        unrenderDocument();
        document.getElementById("pdf_loading_text").style.display = "block";
        await renderDocument(getLokenEdition(counter));
        document.getElementById("pdf_loading_text").style.display = "none";
        for (let element = 0; element < backgroundColorBlob.length; element++) {
            let elementBlob = backgroundColorBlob[element];
            elementBlob.style.transition = "4.6s";
        };
    };
});

// byt bildform button
const bildformButton = document.getElementsByClassName("pdf_nav_buttons")[1];
bildformButton.addEventListener("click", async () => {
    let backgroundColorBlob = document.getElementsByClassName("background_colorblob"); 
    for (let element = 0; element < backgroundColorBlob.length; element++) {
        let elementBlob = backgroundColorBlob[element];
        elementBlob.style.transition = "0s";
    };
    if (renderMode == "browser") {
        renderMode = "JSrender";
        bildformButton.innerText = "byt till browserrendering";
        document.getElementById("main_pdf").style.display = "none";
        document.getElementById("pdf_loading_text").style.display = "block";
        await renderDocument(getLokenEdition(counter));
        document.getElementById("pdf_loading_text").style.display = "none";
    } else {
        renderMode = "browser";
        bildformButton.innerText = "byt till bildrendering";
        pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
        document.getElementById("main_pdf").style.display = "block";
        await unrenderDocument();
    };
    for (let element = 0; element < backgroundColorBlob.length; element++) {
        let elementBlob = backgroundColorBlob[element];
        elementBlob.style.transition = "4.6s";
    };
    console.log("render mode now " + renderMode)
});

// next button
document.getElementsByClassName("pdf_nav_buttons")[2].addEventListener("click", async () => {
    counter += 1;
    if (counter > amoutPDfs) {
        counter = 1;
    };
    PDFHandle();
    if (renderMode == "browser") {
        pdfContent.src = `./pdfs/Östra_Löken_upplaga_${counter}.pdf`;
    } else {
        let backgroundColorBlob = document.getElementsByClassName("background_colorblob"); 
        for (let element = 0; element < backgroundColorBlob.length; element++) {
            let elementBlob = backgroundColorBlob[element];
            elementBlob.style.transition = "4.6s";
        };
        unrenderDocument();
        document.getElementById("pdf_loading_text").style.display = "block";
        await renderDocument(getLokenEdition(counter));
        document.getElementById("pdf_loading_text").style.display = "none";
        for (let element = 0; element < backgroundColorBlob.length; element++) {
            let elementBlob = backgroundColorBlob[element];
            elementBlob.style.transition = "4.6s";
        };
    };
});

function PDFHandle() {
    console.log(pdfContent);
    console.log(counter);
    pdfNumber.innerText = `Upplaga ${counter} / ${amoutPDfs}`;
};