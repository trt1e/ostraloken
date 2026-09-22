const submitForm = document.querySelector("#main-submit-feed");

// Items containing article info
const titleTextItem = document.querySelector("#user-input-rubrik");
const texttypeTextItem = document.querySelector("#user-input-texttyp");
const writerTextItem = document.querySelector("#user-input-skribent");
const articleTextItem = document.querySelector("#user-input-artikel");

submitForm.addEventListener("submit", (event) => {
    event.preventDefault(); // makes site not reload

    // Extract the article info
    const titleExtractedText = titleTextItem.value;
    const texttypeExtractedText = texttypeTextItem.value;
    const writerExtractedText = writerTextItem.value;
    const articleExtractedText = articleTextItem.value;

    // Fill in the template
    fillTemplte(titleExtractedText, texttypeExtractedText, writerExtractedText, articleExtractedText)
});


// Get the template elements that are to be filled
const titleTextTemplateItem = document.querySelector("#title-template-container");
const texttypeTextTemplateItem = document.querySelector("#texttype-template-container");
const writerTextTemplateItem = document.querySelector("#writer-template-container");
const articleTextTemplateItem = document.querySelector("#article-template-container");

function fillTemplte(title, texttype, writer, article) { // This fills in the template elements with their new content
    titleTextTemplateItem.innerText = title;
    texttypeTextTemplateItem.innerText = texttype;
    writerTextTemplateItem.innerText = writer;
    articleTextTemplateItem.innerText = article;
};
