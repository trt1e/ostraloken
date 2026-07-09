const ids = Array.from(document.querySelectorAll('.article')).map(el => el.id); /*copyd from internet*/

const im_feeling_lucky_button_element = document.getElementById("im_feeling_lucky");
im_feeling_lucky_button_element.addEventListener("click", () => {
    const random_article = Math.floor(Math.random() * ids.length); /*the articles ids are the urls of the same articles*/
    console.log("Redirecting to: " + ids[random_article]);
    window.location.href = "https://ostraloken.se/a/" + ids[random_article] + ".html";
});