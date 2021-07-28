from math import sin, cos, atan, asin, sqrt

# TODO need to add adjustment to frame of tiles (left top corner is (0,0), etc)
def latlng_to_orthographic(lat, lng, radius, lat_centre, lng_centre):
    """
    Given a point's latitude and longitude, projection radius, and projection 
    centre in latitude and longitude, return the cartesian x and y coordinates of the 
    orthographic projection.

    ----- Parameters ----
    lat: point's latitude
    lng: point's logitude
    radius: projection radius
    lat_centre: projection centre's latitude
    lng_centre: projection centre's longitude

    ------ Return -------
    tuple(x, y): orthographic cartesian x, y
    """
    x = radius * cos(lat) * sin(lng - lng_centre)
    y = radius * (cos(lat_centre) * sin(lat) - sin(lat_centre) * cos(lat) * cos(lng - lng_centre))
    return x, y

def orthographic_to_latlng(x, y, radius, lat_centre, lng_centre):
    """
    Given the point in cartesian x and y coordinates of the orthographic projection, 
    the projection radius, and projection centre in latitude and longitude,
    return the point in latitude and longitude.

    ----- Parameters ----
    x: orthographic cartesian x
    y: orthographic cartesian y
    radius: projection radius
    lat_centre: projection centre's latitude
    lng_centre: projection centre's longitude

    ------ Return -------
    tuple(lat, lng): latitude, longitude
    """
    rho = sqrt(x ** 2 + y ** 2)
    c = asin(rho/radius)
    lat = asin(cos(c) * sin(lat_centre) + (y * sin(c) * cos(lat_centre)) / rho)
    lng = lng_centre + atan((x * sin(c)) / rho * cos(c) * cos(lat_centre) - y * sin(c) * sin(lat_centre))
    return lat, lng