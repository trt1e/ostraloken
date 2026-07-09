const now_date = get_date();

document.addEventListener("DOMContentLoaded", () => {set_date(now_date)});

function get_date() {
    const date = new Date();
    let new_date_string = "";

    const weekdays = ["Söndag", "Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag"];
    let day = weekdays[date.getDay()];
    new_date_string += day + " ";
    let date_number = date.getDate();
    new_date_string += date_number + " ";
    const months = ["januari", "februari", "mars", "april", "maj", "juni", "juli", "augusti", "september", "oktober", "november", "december"];
    let month = months[date.getMonth()];
    new_date_string += month + " ";
    let year = date.getFullYear();
    new_date_string += year;

    return new_date_string;
};

function set_date(date_given) {
    const date_element = document.getElementById("header_date");
    date_element.innerText = date_given;
    console.log("Setting date to: " + date_given);
};