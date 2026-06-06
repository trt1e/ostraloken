const share_button = document.querySelector("button#share");

share_button.addEventListener("click", async () => {
    if (navigator.canShare()) {
        try {
            await navigator.share(shareData);
            console.log("MDN shared successfully");
        } catch (err) {
            console.log(`Error: ${err}`);
        }
    };
});

window.addEventListener("load", () => {
    if (navigator.canShare()) {
        console.log("Can share!");
    } else {
        console.log("Can't share!");
        share_button.style.display = "none";
    };
});