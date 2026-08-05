document.addEventListener("DOMContentLoaded", () => { 
    let hear_me_outs_storage = localStorage.getItem("hear-me-outs");
    let hear_me_out_statuses = {};
    // hear_me_outs_storage = localStorage.setItem("hear-me-outs", {});

    if (hear_me_outs_storage) {
        hear_me_out_statuses = JSON.parse(hear_me_outs_storage);
    };
    console.log(hear_me_out_statuses);

    console.log(document.querySelectorAll("article.article"))

    for (let hear_me_out_number = 0; hear_me_out_number < document.querySelectorAll("article.article").length; hear_me_out_number++) {
        const smash_button_element = document.getElementsByClassName("smash_button")[hear_me_out_number];
        const pass_button_element = document.getElementsByClassName("pass_button")[hear_me_out_number];

        const specific_article_hear_me_out = document.querySelectorAll("article.article h2")[hear_me_out_number].innerHTML;
        const specific_article_description = document.querySelectorAll("article.article p")[hear_me_out_number].innerHTML;
        const specific_article_id = specific_article_hear_me_out + specific_article_description

        if (hear_me_outs_storage) {
            if (hear_me_out_statuses[specific_article_id] == "Smash") {
                smash_button_element.classList.add("clicked");
            } else if (hear_me_out_statuses[specific_article_id] == "Pass") {
                pass_button_element.classList.add("clicked");
            };
        } else {
            hear_me_out_statuses[specific_article_id] = "None";
        };

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