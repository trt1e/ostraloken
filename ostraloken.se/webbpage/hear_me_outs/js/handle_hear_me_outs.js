/*
GÖR OM HELA DET HÄR SYSTEMET:
Den ska egentligen spara som en {} där den pekar mot vilken id som är smash or pass
Just nu fungerar så länge man inte lägger till fler hear me out:s, men det är precis det vi gör!!
*/

document.addEventListener("DOMContentLoaded", () => { 
    let hear_me_outs_storage = localStorage.getItem("hear-me-outs");
    let hear_me_out_statuses = [];
    // hear_me_outs_storage = localStorage.setItem("hear-me-outs", []);

    if (hear_me_outs_storage) {
        hear_me_out_statuses = JSON.parse(hear_me_outs_storage);
    };
    console.log(hear_me_out_statuses);

    for (let hear_me_out_number = 0; hear_me_out_number < document.getElementsByClassName("article").length; hear_me_out_number++) {
        const smash_button_element = document.getElementsByClassName("smash_button")[hear_me_out_number];
        const pass_button_element = document.getElementsByClassName("pass_button")[hear_me_out_number];

        if (hear_me_outs_storage) {
            if (hear_me_out_statuses[hear_me_out_number] == "Smash") {
                smash_button_element.classList.add("clicked");
            } else if (hear_me_out_statuses[hear_me_out_number] == "Pass") {
                pass_button_element.classList.add("clicked");
            };
        } else {
            hear_me_out_statuses[hear_me_out_number] = "None";
        };

        smash_button_element.addEventListener("click", () => {
            if (hear_me_out_statuses[hear_me_out_number] == "Smash") {
                hear_me_out_statuses[hear_me_out_number] = "None";
                smash_button_element.classList.remove("clicked");
            } else {
                hear_me_out_statuses[hear_me_out_number] = "Smash";
                smash_button_element.classList.add("clicked");
                pass_button_element.classList.remove("clicked");
            };
            console.log("Smash button pressed");
            localStorage.setItem("hear-me-outs", JSON.stringify(hear_me_out_statuses));
            console.log(hear_me_out_statuses);
        });
        pass_button_element.addEventListener("click", () => {
            if (hear_me_out_statuses[hear_me_out_number] == "Pass") {
                hear_me_out_statuses[hear_me_out_number] = "None";
                pass_button_element.classList.remove("clicked");
            } else {
                hear_me_out_statuses[hear_me_out_number] = "Pass";
                pass_button_element.classList.add("clicked");
                smash_button_element.classList.remove("clicked");
            };
            console.log("Pass button pressed");
            localStorage.setItem("hear-me-outs", JSON.stringify(hear_me_out_statuses));
            console.log(hear_me_out_statuses);
        });
    };
});