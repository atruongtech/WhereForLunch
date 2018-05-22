from Configuration.google_config import base_url, api_key
import requests


def get_travel_time(restaurant, address):
    travel_json = __get_distance_data(restaurant, address)
    if travel_json["status"] == "OK":
        return travel_json["rows"][0]["elements"][0]["duration"]["text"]
    else:
        return None


def __get_distance_data(restaurant, address):
    params = {"origins": address, "destinations": restaurant.address, "key": api_key}
    response = requests.get(base_url, params)
    return response.json()
