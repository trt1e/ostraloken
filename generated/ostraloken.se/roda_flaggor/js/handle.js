document.addEventListener("DOMContentLoaded", () => { 
    let roda_flaggor_storage = localStorage.getItem("roda-flaggor-storage"); // We get the local storage item roda-flaggor-storage
    let roda_flaggor_statuses = {}; // Create a empty dict with the status of all roda flaggor
    // roda_flaggor_storage = localStorage.setItem("roda-flaggor-storage", {});

    if (roda_flaggor_storage) { // If there is something in that local storage
        roda_flaggor_statuses = JSON.parse(roda_flaggor_storage); // in that case we parse the storage into the previosly created status dict 
    };
    console.log(roda_flaggor_statuses);

    const all_article_elements = document.querySelectorAll("article.rod_flagga") // We get all roda flaggor article elements

    // We loop through all the roda flaggor articles  
    for (let rod_flagga_number = 0; rod_flagga_number < all_article_elements.length; rod_flagga_number++) {
        const article_element = all_article_elements[rod_flagga_number]; // We get this specific article
        
        const smash_button_element = article_element.getElementsByClassName("smash_button")[0]; // We get that articles smash button as a element
        const pass_button_element = article_element.getElementsByClassName("pass_button")[0]; // We get that articles pass button as a element

        const specific_article_rod_flagga = article_element.querySelectorAll("h2")[0].innerHTML; // We get that articles rod flagga text
        const specific_article_description = article_element.querySelectorAll("p")[0].innerHTML; // We get that articles rod flagga description
        const specific_article_id = specific_article_rod_flagga + specific_article_description // We create a rod flagga id using the hmo text and description

        // We go through and "click" the elements that are supposed to be clicked according to the storage file gatherd from local storage
        if (roda_flaggor_storage) { // If there is something in that local storage
            if (roda_flaggor_statuses[specific_article_id] == "Smash") {
                smash_button_element.classList.add("clicked");
            } else if (roda_flaggor_statuses[specific_article_id] == "Pass") {
                pass_button_element.classList.add("clicked");
            };
        } else { // If rod flagga storage dosn't have any content we can just set the elements status to None
            roda_flaggor_statuses[specific_article_id] = "None";
            localStorage.setItem("roda-flaggor-storage", JSON.stringify(roda_flaggor_statuses));
            console.log(roda_flaggor_statuses);
        };

        // Now we add triger events on the smash and pass buttons if they are clicked
        smash_button_element.addEventListener("click", () => {
            if (roda_flaggor_statuses[specific_article_id] == "Smash") {
                roda_flaggor_statuses[specific_article_id] = "None";
                smash_button_element.classList.remove("clicked");
            } else {
                roda_flaggor_statuses[specific_article_id] = "Smash";
                smash_button_element.classList.add("clicked");
                pass_button_element.classList.remove("clicked");
            };
            console.log("Smash button pressed");
            localStorage.setItem("roda-flaggor-storage", JSON.stringify(roda_flaggor_statuses));
            console.log(roda_flaggor_statuses);
        });
        pass_button_element.addEventListener("click", () => {
            if (roda_flaggor_statuses[specific_article_id] == "Pass") {
                roda_flaggor_statuses[specific_article_id] = "None";
                pass_button_element.classList.remove("clicked");
            } else {
                roda_flaggor_statuses[specific_article_id] = "Pass";
                pass_button_element.classList.add("clicked");
                smash_button_element.classList.remove("clicked");
            };
            console.log("Pass button pressed");
            localStorage.setItem("roda-flaggor-storage", JSON.stringify(roda_flaggor_statuses));
            console.log(roda_flaggor_statuses);
        });
    };
});