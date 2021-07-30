
function latlng_to_orthographic(lat, lng, radius, lat_centre, lng_centre) {
    let x = radius * Math.cos(lat) * Math.sin(lng - lng_centre)
    let y = radius * (Math.cos(lat_centre) * Math.sin(lat) - Math.sin(lat_centre) * Math.cos(lat) * Math.cos(lng - lng_centre))
    return [x, y]
}

function orthographic_to_latlng(x, y, radius, lat_centre, lng_centre) {
    let rho = Math.sqrt(x ** 2 + y ** 2)
    let c = Math.asin(rho/radius)
    let lat = Math.asin(Math.cos(c) * Math.sin(lat_centre) + (y * Math.sin(c) * Math.cos(lat_centre)) / rho)
    let lng = lng_centre + Math.atan((x * Math.sin(c)) / rho * Math.cos(c) * Math.cos(lat_centre) - y * Math.sin(c) * Math.sin(lat_centre))
    return [lat, lng]
}


var mainMap = L.map('mainMap', {
    crs: L.CRS.Simple, // simple square grid, need to finure out some curvy grid
    minZoom: -5,
    layers: background
    });

const skymapDir = "../skymaps/";
const PlanckDir = skymapDir + "Planck_30GHz_galactic_4096/";
const MRSDir = "../2MASS_images/"

// var bounds = [[-100, -195], [100, 195]]; 
var bounds = [[-100, -100], [100, 100]];

var background = L.imageOverlay(PlanckDir + "northpole.png", bounds).addTo(mainMap);
// var background = L.imageOverlay(MRSDir + "LongLat_projected.png", bounds).addTo(mainMap);
mainMap.fitBounds(bounds);

function onEachFeature(feature, layer) {
		var popupContent = "I come from geoJSON. "; //"<p>I started out as a GeoJSON " +
				// feature.geometry.type + ", but now I'm a Leaflet vector!</p>";

		if (feature.properties && feature.properties.popupContent) {
			popupContent += feature.properties.popupContent;
		}

		layer.bindPopup(popupContent);
	}

L.geoJSON(objects, {
		pointToLayer: function (feature, latlng) {
            const ortho = latlng_to_orthographic(latlng[0], latlng[1], 1, 90, 0);
			return L.marker(L.latlng(ortho[0], ortho[1])); 
            // return L.marker(latlng);
		},
		onEachFeature: onEachFeature
	}).addTo(mainMap);

// L.geoJSON(footprints, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);

// L.geoJSON(des, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);