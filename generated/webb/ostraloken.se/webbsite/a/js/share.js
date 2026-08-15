const share_button = document.querySelector("button#share");
const share_data = {
    title: document.querySelector("article.article .type_text").innerText + ": " + document.querySelector("article.article h1").innerText + " | Östra Löken",
    url: window.location.href
};

share_button.addEventListener("click", async () => {
    if (navigator.canShare(share_data)) {
        try {
            await navigator.share(share_data);
            console.log("Shared successfully");
        } catch (err) {
            console.log(`Error: ${err}`);
        }
    };
});

// unload the share button if the page cannot be shared this way
window.addEventListener("load", () => {
    if (navigator.canShare(share_data)) {
        console.log("Can share!");
    } else {
        console.log("Can't share!");
        share_button.style.display = "none";
    };
});