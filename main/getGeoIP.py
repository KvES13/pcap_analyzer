import os
import geoip2.database


def find_path(file_name):
    cur_dir = os.getcwd()

    tree = os.walk(cur_dir)
    for address, dirs, files in tree:
        if file_name in files:
            path = address
            break

    if os.name == "posix":
        return path + "/" + file_name
    else:
        return path + "\\" + file_name


path = find_path('GeoLite2-City.mmdb')
reader = geoip2.database.Reader(path)


def get_geo(ip):
    '''return [continent, country, region, city, longitude, latitude]'''
    struct = {
        "continent": "No Data",
        "country": "No Data",
        "region": "No Data",
        "city": "No Data",
        "long": 0,
        "lat": 0
    }
    try:
        response = reader.city(ip)
        country_name = "No Data"
        city_name = "No Data"
        continent_name = "No Data"
        region_name = "No Data"
        if 'ru' in response.country.names.keys():
            country_name = response.country.names['ru']
        if 'ru' in response.city.names.keys():
            city_name = response.city.names['ru']
        if 'ru' in response.continent.names.keys():
            continent_name = response.continent.names['ru']
        if len(response.subdivisions) > 0:
            if 'ru' in response.subdivisions[0].names.keys():
                region_name = response.subdivisions[0].names["ru"]
        longitude = response.location.latitude
        latitude = response.location.longitude

        struct["continent"] = continent_name
        struct["country"] = country_name
        struct["region"] = region_name
        struct["city"] = city_name
        struct["long"] = longitude
        struct["lat"] = latitude
        return struct

    except:
        return struct


if __name__ == '__main__':
    print(get_geo("82.102.16.174"))
