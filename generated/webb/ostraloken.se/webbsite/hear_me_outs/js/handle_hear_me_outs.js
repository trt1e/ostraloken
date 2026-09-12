document.addEventListener("DOMContentLoaded", () => { 
    let hear_me_outs_storage = localStorage.getItem("hear-me-outs"); // We get the local storage item hear-me-outs
    let hear_me_out_statuses = {}; // Create a empty dict with the status of all hear me outs
    // hear_me_outs_storage = localStorage.setItem("hear-me-outs", {});

    if (hear_me_outs_storage) { // If there is something in that local storage
        hear_me_out_statuses = JSON.parse(hear_me_outs_storage); // in that case we parse the storage into the previosly created status dict 
    };
    console.log(hear_me_out_statuses);

    // We loop through all the hear me out articles  
    for (let hear_me_out_number = 0; hear_me_out_number < document.querySelectorAll("article.article").length; hear_me_out_number++) {
        const smash_button_element = document.getElementsByClassName("smash_button")[hear_me_out_number]; // We get that articles smash button as a element
        const pass_button_element = document.getElementsByClassName("pass_button")[hear_me_out_number]; // We get that articles pass button as a element

        const specific_article_id = "HMO_id_" + hear_me_out_number

        // We go through and "click" the elements that are supposed to be clicked according to the storage file gatherd from local storage
        if (hear_me_outs_storage) { // If there is something in that local storage
            if (hear_me_out_statuses[specific_article_id] == "Smash") {
                smash_button_element.classList.add("clicked");
            } else if (hear_me_out_statuses[specific_article_id] == "Pass") {
                pass_button_element.classList.add("clicked");
            };
        } else { // If hear me out storage dosn't have any content we can just set the elements status to None
            hear_me_out_statuses[specific_article_id] = "None";
        };

        // Now we add triger events on the smash and pass buttons if they are clicked
        smash_button_element.addEventListener("click", () => {
            if (hear_me_out_statuses[specific_article_id] == "Smash") {
                hear_me_out_statuses[specific_article_id] = "None";
                smash_button_element.classList.remove("clicked");
            } else {
                hear_me_out_statuses[specific_article_id] = "Smash";
                smash_button_element.classList.add("clicked");
                pass_button_element.classList.remove("clicked");
            };
            console.log("Smash button pressed");
            localStorage.setItem("hear-me-outs", JSON.stringify(hear_me_out_statuses));
            console.log(hear_me_out_statuses);
        });
        pass_button_element.addEventListener("click", () => {
            if (hear_me_out_statuses[specific_article_id] == "Pass") {
                hear_me_out_statuses[specific_article_id] = "None";
                pass_button_element.classList.remove("clicked");
            } else {
                hear_me_out_statuses[specific_article_id] = "Pass";
                pass_button_element.classList.add("clicked");
                smash_button_element.classList.remove("clicked");
            };
            console.log("Pass button pressed");
            localStorage.setItem("hear-me-outs", JSON.stringify(hear_me_out_statuses));
            console.log(hear_me_out_statuses);
        });
    };
});