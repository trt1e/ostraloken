const HH_MM = {hour: '2-digit', minute: '2-digit' };
// base: https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/<parameter>/station/<stationId>/period/latest-hour/data.json
const SMHIFetchLink = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station/98230/period/latest-hour/data.json";

window.onscroll = function() {progressbar_uppdate()};
window.onload = function() {
    progressbar_uppdate()
    time_update()
    date_update()
    wether_update()
};
setInterval(time_update, 1000);
setInterval(date_update, 60000); // uppdate every 20min

// uppdatera progress bar
function progressbar_uppdate() {
    let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    let height = document.body.scrollHeight - window.innerHeight;
    let scrolled = (winScroll / height) * 100;

    document.getElementById("top_progress_bar").style.width = scrolled + "%";
};

// för att uppdatera tiden i headern
function time_update() {
    let time_hours = new Date().getHours()
    let time_min = new Date().getMinutes()

    /*
    if (getLength(time_min) = 1) { //funkar inte, fuckar hela
        time_min = "0" + time_min
    }
    */

    document.getElementById("header_time").innerHTML = time_hours + ":" + time_min;
};

// för att uppdatera datumet i headern
function date_update() {
    let date_year = new Date().getFullYear()
    let date_month = new Date().getMonth()
    let date_date = new Date().getDate()
    let date = (date_date + "/" + date_month + "/" + date_year)

    document.getElementById("header_date").innerHTML = date;
};

// för att uppdatera vädret i headern (görs bara när sidan ladas in)
async function wether_update() {
    try {
        const response = await fetch(SMHIFetchLink);
        if (!response.ok) {
        throw new Error("Nätverksfel: " + response.status);
        }
        const data = await response.json();
        const temperature = data.value[0].value; // <-- här ligger temperaturen
        document.getElementById("header_wether").innerHTML = `${temperature} °C`;

        return temperature;
    } catch (error) {
        console.error("Fel vid hämtning av temperatur:", error);
    }
};