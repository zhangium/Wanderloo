getLocation();

var trail = 0;
var distance = 0;
var route = 0;
var winter = 0;
var position_lat = "-80.5441129";
var position_lon = "43.4705486";

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else { 
        document.getElementById("position").innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    //document.getElementById("position").innerHTML = "Latitude: " + position.coords.latitude + "<br>Longitude: " + position.coords.longitude;
    // position_lon = position.coords.latitude.toString();
    // position_lat = position.coords.longitude.toString();
    document.getElementById("position").innerHTML = "You're at: (" + position.coords.latitude + ", " + position.coords.longitude + ")";
}

function submit_button() {
	trail = document.getElementById("trail_type").value;
	distance = document.getElementById("distance").value;
	route = document.getElementById("on_bus_route").value;
	winter = document.getElementById("cleared_in_winter_by").value;
	document.cookie = "enghackskip=0,enghacksurface="+trail+",enghackdistance="+distance+",enghackonbusroute="+route+",enghackwinter="+winter+",enghackposition="+position_lat+"X"+position_lon+";expires=Thu, 01 Jan 2018 00:00:00 GMT;domain=uwaterloo.ca;path=/";
    document.getElementById("btn").innerHTML = "Loading";
    setTimeout(change_page,3000);
}

function change_page() {
    window.location.href = "http://www.eng.uwaterloo.ca/~mc26wong/map.html";
}