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

    // Add the comments
    addComments(titleExtractedText, texttypeExtractedText, writerExtractedText, articleExtractedText);

    // Fill in the template
    fillTemplte(titleExtractedText, texttypeExtractedText, writerExtractedText, articleExtractedText);

    // Export the txt-formated article
    formatArticle(titleExtractedText, texttypeExtractedText, writerExtractedText, articleExtractedText);
});


// Check if the text flaggs anything wrong or out of order
function videCheckText(text) {
    let allComments = "";

    // First we check if the right citationmarks are used
    if (text.includes('"')) {
        allComments += `NOTERA: " används, du bör använda ”\n`
    };
    if (text.includes('“')) {
        allComments += `NOTERA: “ används, du bör använda ”\n`
    };
    if (text.includes("'")) {
        allComments += `NOTERA: ' används, du bör använda ’\n`
    };
    if (text.includes("‘")) {
        allComments += `NOTERA: ‘ används, du bör använda ’\n`
    };

    // We check so that there is no . before a citationmark
    if (text.includes('."') || text.includes('.“') || text.includes('.”') || text.includes(".'") || text.includes(".‘") || text.includes(".’")) {
        allComments += `NOTERA: . är placerad innan citattecken, så gör vi inte i svenskan utan den hamnar utanför\n`
    };
    
    // We check so that there is no , before a citationmark
    if (text.includes(',"') || text.includes(',“') || text.includes(',”') || text.includes(",'") || text.includes(",‘") || text.includes(",’")) {
        allComments += `NOTERA: , är placerad innan citattecken, så gör vi inte i svenskan utan den hamnar utanför\n`
    };

    // Check if there is a "-" with both sides empty
    if (text.includes(" - ")) {
        allComments += `NOTERA: - används som ett –\n`
    };

    return allComments;
};

// Get the comment elements that are to be filled
const titleCommentItem = document.querySelector("#output-rubrik");
const texttypeCommentItem = document.querySelector("#output-texttyp");
const writerCommentItem = document.querySelector("#output-skribent");
const articleCommentItem = document.querySelector("#output-artikel");

function addComments(title, texttype, writer, article) { // This adds the comments to the text
    // Check the title:
    let titleComment = videCheckText(title);
    if (title.length > 100) {
        titleComment +=  `NOTERA: Rubriken är ${title.length} karaktärer lång, och det är lite långt\n`
    };

    // Check the texttype:
    let texttypeComment = videCheckText(texttype);
    if (texttype.length > 22) {
        texttypeComment +=  `NOTERA: Texttypen är ${texttype.length} karaktärer lång, och det är lite långt\n`
    };
    
    // Check the writer:
    let writerComment = videCheckText(writer);
    if (writer.length > 30) {
        writerComment +=  `NOTERA: Skribentens namn är ${writer.length} karaktärer lång, och det är lite långt\n`
    };
    
    // Check the article:
    let articleComment = videCheckText(article);
    
    // Then send the comments back
    titleCommentItem.innerText = titleComment;
    texttypeCommentItem.innerText = texttypeComment;
    writerCommentItem.innerText = writerComment;
    articleCommentItem.innerText = articleComment;
};


// Get the template elements that are to be filled
const titleTemplateItem = document.querySelector("#title-template-container");
const texttypeTemplateItem = document.querySelector("#texttype-template-container");
const writerTemplateItem = document.querySelector("#writer-template-container");
const articleTemplateItem = document.querySelector("#article-template-container");

function fillTemplte(title, texttype, writer, article) { // This fills in the template elements with their new content
    titleTemplateItem.innerText = title;
    texttypeTemplateItem.innerText = texttype;
    writerTemplateItem.innerText = writer;
    articleTemplateItem.innerText = article;
};


// Get the format elements that are to be filled
const wholeArticleFormatedItem = document.querySelector("#formated-article");

function formatArticle(title, texttype, writer, article) { // This fills in the template elements with their new content
    const outputText = `>>Rubrik: ${title}
>>Texttyp: ${texttype}
>>Skribent: ${writer}
>>Artikel: 
${article}`

    wholeArticleFormatedItem.value = outputText;
};
