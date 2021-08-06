class ProjectedObject {
    constructor(latlng, proj, radius) {
        this.proj = proj
        this.proj_centre = this.getCentre()   
        this.latLng = latlng     
        this.radius = radius
        this.coords = this.convertCoords()
        this.visibleCoords = this.getVisiblePoints()
        // this.info ?        
    }

    getCentre() {
        if (this.proj == "north") {
            return [90, 0]
        } else if (this.proj == "south") {
            return [-90, 0]
        } else if (this.proj == "meridian") {
            return [0, 0]
        } else if (this.proj == "antimeridian") {
            return [0, 180]
        } else if (this.proj == "offaxis") {
            return [45, 45]
        } else if (this.proj == "antioffexis") {
            return [-45, 215]
        } else {
            console.log("Invalid Projection!!")
            // raise InvalidProjection (TODO)
        }
    }

    isVisible(latlng) {
        if (this.proj == "north" && latlng.lat >= 0 && latlng.lat <= 90 && latlng.lng >= -90 && latlng.lng <= 90) {
            return true
        } else if (this.proj == "south" && latlng.lat >= -90 && latlng.lat <= 0 && latlng.lng >= -90 && latlng.lng <= 90) {
            return true
        } else if (this.proj == "meridian" && latlng.lat >= -90 && latlng.lat <= 90 && latlng.lng >= -90 && latlng.lng <= 90) {
            return true
        } else if (this.proj == "antimeridian" && latlng.lat >= -90 && latlng.lat <= 90 && 
        ((latlng.lng >= 90 && latlng.lng <= 180) || (latlng.lng >= -180 && latlng.lng <= -90))) { // TODO test the multi-line thing
            return true
        // } else if (this.proj == "offaxis") {
        //     return true
        // } else if (this.proj == "antioffexis") {
        //     return true
        } else {
            return false
        }
    }

    latlng_to_orthographic(latlng, radius, lat_centre, lng_centre) {
        // TODO add check to not allow out-of-range locations according to which map
        // degrees to radians 
        const lat = latlng.lat * Math.PI / 180
        const lng = latlng.lng * Math.PI / 180
        lat_centre = lat_centre * Math.PI / 180
        lng_centre = lng_centre * Math.PI / 180
        const x = radius * Math.cos(lat) * Math.sin(lng - lng_centre)
        const y = radius * (Math.cos(lat_centre) * Math.sin(lat) - Math.sin(lat_centre) * Math.cos(lat) * Math.cos(lng - lng_centre))
        // return [y, -x] // latlng
        return L.latLng(y, -x)
    }

    orthographic_to_latlng(x, y, radius, lat_centre, lng_centre) {
        const rho = Math.sqrt(x ** 2 + y ** 2)
        const c = Math.asin(rho/radius)
        const lat = Math.asin(Math.cos(c) * Math.sin(lat_centre) + (y * Math.sin(c) * Math.cos(lat_centre)) / rho)
        const lng = lng_centre + Math.atan((x * Math.sin(c)) / rho * Math.cos(c) * Math.cos(lat_centre) - y * Math.sin(c) * Math.sin(lat_centre))
        return [lat, lng]
    }

    convertCoords() {
        return this.latlng_to_orthographic(this.latLng, this.radius, this.proj_centre[0], this.proj_centre[1])
    }

    getVisiblePoints() {
        if (this.isVisible(this.latLng)) {
            return this.latlng_to_orthographic(this.latLng, this.radius, this.proj_centre[0], this.proj_centre[1])
        }   
    }

    get visiblePoints() {
        return this.visibleCoords
    }


}

// class ProjectedFootprint extends ProjectedObject {
//     // store as leaflet polyugon
//     // accept all leaflet info 

//     convertCoords() {
//         let converted = []
//         for (let i = 0; i < this.coords.length; i++) {

//         }
//         return this.latlng_to_orthographic(this.latLng, this.radius, this.proj_centre[0], this.proj_centre[1])
//     }

//     getVisiblePoints() {
//         if (this.isVisible()) {
//             return this.latlng_to_orthographic(this.latLng, this.radius, this.proj_centre[0], this.proj_centre[1])
//         }   
//     }

    
// }

// class ProjectedPoint extends ProjectedObject {

// }

// --------------------------------------------------------------------------------


// function latlng_to_orthographic(lat, lng, radius, lat_centre, lng_centre) {
//     // TODO add check to not allow out-of-range locations according to which map
//     // degrees to radians 
//     lat = lat * Math.PI / 180
//     lng = lng * Math.PI / 180
//     lat_centre = lat_centre * Math.PI / 180
//     lng_centre = lng_centre * Math.PI / 180
//     const x = radius * Math.cos(lat) * Math.sin(lng - lng_centre)
//     const y = radius * (Math.cos(lat_centre) * Math.sin(lat) - Math.sin(lat_centre) * Math.cos(lat) * Math.cos(lng - lng_centre))
//     // return [y, -x] // latlng
//     return L.latLng(y, -x)
// }

// function orthographic_to_latlng(x, y, radius, lat_centre, lng_centre) {
//     const rho = Math.sqrt(x ** 2 + y ** 2)
//     const c = Math.asin(rho/radius)
//     const lat = Math.asin(Math.cos(c) * Math.sin(lat_centre) + (y * Math.sin(c) * Math.cos(lat_centre)) / rho)
//     const lng = lng_centre + Math.atan((x * Math.sin(c)) / rho * Math.cos(c) * Math.cos(lat_centre) - y * Math.sin(c) * Math.sin(lat_centre))
//     return [lat, lng]
// }


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
            // const ortho = latlng_to_orthographic(latlng.lat, latlng.lng, 100, 90, 0);
			// return L.marker(L.latLng(ortho[0], ortho[1])); 

            //feature. whatever property

            let point = new ProjectedObject(latlng, "north", 100)
            // return L.marker(point.coords);
            return L.marker(point.visiblePoints);
		},
		onEachFeature: onEachFeature
	}).addTo(mainMap);

// L.geoJSON(footprints, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);

// L.geoJSON(des, {
//         onEachFeature: onEachFeature
//     }).addTo(MRSmap2);