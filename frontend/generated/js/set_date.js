document.addEventListener("DOMContentLoaded", () => {set_date()});

function set_date() {
    const date_element = document.getElementById("header_date");
    const date = new Date();
    let new_date_string = "";

    const weekdays = ["Söndag", "Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag"];
    let day = weekdays[date.getDay()];
    new_date_string += day + " ";
    let date_number = date.getDate();
    new_date_string += date_number + " ";
    const months = ["Januari", "Februari", "Mars", "April", "Maj", "Juni", "Juli", "Augusti", "September", "Oktober", "November", "December"];
    let month = months[date.getMonth()];
    new_date_string += month;

    date_element.innerText = new_date_string;
    console.log("Setting date to: " + new_date_string);
};