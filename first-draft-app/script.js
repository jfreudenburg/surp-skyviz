
function latlng_to_orthographic(lat, lng, radius, lat_centre, lng_centre) {
    // TODO add check to not allow out-of-range locations according to which map
    // degrees to radians 
    lat = lat * Math.PI / 180
    lng = lng * Math.PI / 180
    lat_centre = lat_centre * Math.PI / 180
    lng_centre = lng_centre * Math.PI / 180
    const x = radius * Math.cos(lat) * Math.sin(lng - lng_centre)
    const y = radius * (Math.cos(lat_centre) * Math.sin(lat) - Math.sin(lat_centre) * Math.cos(lat) * Math.cos(lng - lng_centre))
    // return [y, -x] // latlng
    return L.latLng(y, -x)
}

function orthographic_to_latlng(x, y, radius, lat_centre, lng_centre) {
    const rho = Math.sqrt(x ** 2 + y ** 2)
    const c = Math.asin(rho/radius)
    const lat = Math.asin(Math.cos(c) * Math.sin(lat_centre) + (y * Math.sin(c) * Math.cos(lat_centre)) / rho)
    const lng = lng_centre + Math.atan((x * Math.sin(c)) / rho * Math.cos(c) * Math.cos(lat_centre) - y * Math.sin(c) * Math.sin(lat_centre))
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
var bounds = [[-100, 100], [100, -100]];

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
            const ortho = latlng_to_orthographic(latlng.lat, latlng.lng, 100, 90, 0);
			// return L.marker(L.latLng(ortho[0], ortho[1])); 
            return L.marker(ortho);
		},
		onEachFeature: onEachFeature
	}).addTo(mainMap);

// L.geoJSON(footprints, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);

// L.geoJSON(des, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);