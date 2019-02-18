#This program adds location-markers to map by inputting twitter account

import folium
from geopy import Nominatim
import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl


def decode(string):
    return "".join(list(map(lambda x: chr(ord(x)), string)))


def find_coordinates(place):
    """

    str -> (number, number)

    Return coordinates of the place

    """
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    location = geolocator.geocode(place)
    return location.latitude, location.longitude


def create_twitter_json(acct, path):
    """

    (str, str) -> None

    Create json with twitter account data

    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '5'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    with open(path, 'w', encoding='utf-8', errors='ignore') as file:
        json.dump(js, file, indent=4)


def find_locations(js):
    """

    str -> list

    Return the list of locations and screen names

    """
    with open(js, encoding='utf-8', errors='ignore') as file:
        users = json.loads(file.read())["users"]
    locations = []
    for user in users:
        location = decode(user["location"])
        screen_name = decode(user["screen_name"])
        locations.append((location, screen_name + ', ' + location))
    return locations


def check_coordinates(places):
    """

    list -> list

    Return the list of the coordinates of the places
    """
    coordinates = []
    for place in places:
        try:
            coordinates.append((find_coordinates(place[0]), place[1]))
        except:
            pass
    return coordinates


def add_locations_to_map(mapa, coordinates):
    """
    (Map, list) -> None

    Add Location-Markers to map

    """
    for coordinate in coordinates:
        mapa.add_child(folium.Marker(location=coordinate[0],
                                     popup=coordinate[1],
                                     icon=folium.Icon()))


if __name__ == "__main__":
    account = input("Enter an account: ")
    create_twitter_json(account, "account_data.json")
    locations = find_locations("account_data.json")
    coordinates = check_coordinates(locations)
    mapa = folium.Map()
    add_locations_to_map(mapa, coordinates)
    mapa.save("Map.html")