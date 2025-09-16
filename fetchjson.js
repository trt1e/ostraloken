window.onload() = function {

}


function loadTestFunction() {
    fetch("./articles.json")
    .then(response => response.json())
    .then(data => {
        // 'data' is now an array of your article objects
        const mostRecentArticle = data[0]; // The first item is the most recent
        
        // Find the element on your page where you want to display the article
        const articleContainer = document.getElementById("article");
        
        // Populate the HTML with the data from the JSON file
        articleContainer.innerHTML = `
            <h2>${mostRecentArticle.title}</h2>
            <img src="${mostRecentArticle.image}" alt="${mostRecentArticle.title}">
            <p>${mostRecentArticle.content}</p>
        `;
    })
    .catch(
        error => console.error("Could not fetch articles:", error),
        alert(e)
    );
}