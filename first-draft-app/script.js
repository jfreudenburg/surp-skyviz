// import "https://unpkg.com/leaflet@1.7.1/dist/leaflet.js";
document.writeln('<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>');

function latlng_to_orthographic(lat, lng, radius, lat_centre, lng_centre) {
    let x = radius * Math.cos(lat) * Math.sin(lng - lng_centre)
    let y = radius * (Math.cos(lat_centre) * Math.sin(lat) - Math.sin(lat_centre) * Math.cos(lat) * Math.cos(lng - lng_centre))
    return x, y
}

function orthographic_to_latlng(x, y, radius, lat_centre, lng_centre) {
    let rho = Math.sqrt(x ** 2 + y ** 2)
    let c = Math.asin(rho/radius)
    let lat = Math.asin(Math.cos(c) * Math.sin(lat_centre) + (y * Math.sin(c) * Math.cos(lat_centre)) / rho)
    let lng = lng_centre + Math.atan((x * Math.sin(c)) / rho * Math.cos(c) * Math.cos(lat_centre) - y * Math.sin(c) * Math.sin(lat_centre))
    return lat, lng
}


var mainMap = L.map('mainMap', {
    crs: L.CRS.Simple, // simple square grid, need to finure out some curvy grid
    minZoom: -5,
    layers: background
    });

const skymapDir = "../skymaps/";
const PlanckDir = skymapDir + "Planck_30GHz_galactic_4096/";

console.log(PlanckDir);

var bounds = [[-100, -195], [100, 195]]; // set proper

var background = L.imageOverlay(PlanckDir + "northpole.png", bounds).addTo(mainMap);
mainMap.fitBounds(bounds);

//     mainMap.setView( [0, 0], 1.25);

//     var sunIcon = L.icon({
//     iconUrl: 'misc_images/angrySun.png',
//     iconSize:     [100, 60], // size of the icon
//     iconAnchor:   [50, 30], // point of the icon which will correspond to marker's location
//     popupAnchor:  [0, 0] // point from which the popup should open relative to the iconAnchor
// });

// function onEachFeature(feature, layer) {
// 		var popupContent = "I come from geoJSON. "; //"<p>I started out as a GeoJSON " +
// 				// feature.geometry.type + ", but now I'm a Leaflet vector!</p>";

// 		if (feature.properties && feature.properties.popupContent) {
// 			popupContent += feature.properties.popupContent;
// 		}

// 		layer.bindPopup(popupContent);
// 	}

// L.geoJSON(objects, {
// 		pointToLayer: function (feature, latlng) {
// 			return L.marker(latlng, {icon: sunIcon});
// 		},
// 		onEachFeature: onEachFeature
// 	}).addTo(MRSmap2);

// L.geoJSON(footprints, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);

// L.geoJSON(des, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);