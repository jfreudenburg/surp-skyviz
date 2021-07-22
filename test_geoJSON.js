var footprints = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[0, 10], [5, 20], [20, 40], [10, 20], [5, -5]], 
                    [[-10, -10], [-10, -20], [-5, -15]]
            ]
            },
            "properties": {
                "popupContent": "This is an example survey footprints."
            },
            "id": 1
        } //,
        // {
        //     "type": "Feature",
        //     "geometry": {
        //         "type": "LineString",
        //         "coordinates": [
        //             [-105.0008225440979, 39.751891803969535],
        //             [-104.99820470809937, 39.74979664004068]
        //         ]
        //     },
        //     "properties": {
        //         "popupContent": "This is a free bus line that will take you across downtown."
        //     },
        //     "id": 2
        // },
        // {
        //     "type": "Feature",
        //     "geometry": {
        //         "type": "LineString",
        //         "coordinates": [
        //             [-104.99820470809937, 39.74979664004068],
        //             [-104.98689651489258, 39.741052354709055]
        //         ]
        //     },
        //     "properties": {
        //         "popupContent": "This is a free bus line that will take you across downtown.",
        //         "underConstruction": false
        //     },
        //     "id": 3
        // }
    ]
};

var objects = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "popupContent": "supposed to be at x: 0, y: 90"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [90, 0]
            }
        },{
            "type": "Feature",
            "properties": {
                "popupContent": "supposed to be at x: 0, y: 0"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [0, 0]
            }
        }
    ]
};