from math import sin, cos, atan, asin, sqrt

def latlng_to_orthographic(lat, lng, radius, lat_centre, lng_centre):
    x = radius * cos(lat) * sin(lng - lng_centre)
    y = radius * (cos(lat_centre) * sin(lat) - sin(lat_centre) * cos(lat) * cos(lng - lng_centre))
    return x, y

def orthographic_to_latlng(x, y, radius, lat_centre, lng_centre):
    rho = sqrt(x ** 2 + y ** 2)
    c = asin(rho/radius)
    lat = asin(cos(c) * sin(lat_centre) + (y * sin(c) * cos(lat_centre)) / rho)
    lng = lng_centre + atan((x * sin(c)) / rho * cos(c) * cos(lat_centre) - y * sin(c) * sin(lat_centre))
    return lat, lng