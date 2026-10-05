
var map = L.map('map').setView([51.505, -0.09], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

fetch(allCharitiesURL).then(resp => resp.json()).then(addCharitiesToMap)

/*var marker = L.marker([51.5, -0.09]).addTo(map);
var marker2 = L.marker([51.508, -0.11]).addTo(map);

var circle = L.circle([51.5, -0.09], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: 500
}).addTo(map);

marker.bindPopup("<b>Hello world!</b><br>I am a popup.").openPopup();
*/

function addCharitiesToMap(data){
    for (let d of data) {
        if (d.latitude && d.longitude) {
            let m = L.marker([d.latitude, d.longitude]).addTo(map)
            m.bindPopup(`<div onclick="location.href='${SCRIPT_ROOT}/charity/${d.charity_id}';" style="cursor: pointer;">
                <h3>${d.charity_name}</h3>
                <a href='${d.url}'> ${d.url} </a>
                <br>
                <br>
                location: ${d.location_name}
                <br>
                <br>
                summary: ${d.summary}
                <br>

                </div>`).openPopup()
        }
    }    
}
