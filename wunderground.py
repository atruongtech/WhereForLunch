from Configuration.wunderground_config import api_key, endpoint_url_base, target_city
import datetime
import json
import requests

temperature_key = "feelslike_f"

__cache_file_path = "./Configuration/weather_cache.json"


def __is_cache_valid(weather_data):
    weather_epoch = int(weather_data["current_observation"]["observation_epoch"])
    current_datetime = datetime.datetime.now()
    observation_datetime = datetime.datetime.fromtimestamp(weather_epoch)
    return observation_datetime > current_datetime - datetime.timedelta(hours=5)


def __read_cache():
    try:
        with open(__cache_file_path, "r") as weather_cache:
            weather_data = json.load(weather_cache)
            if __is_cache_valid(weather_data):
                return weather_data
            else:
                return None
    except FileNotFoundError:
        return None


def __write_cache(weather_data):
    with open(__cache_file_path, "w") as weather_cache:
        json.dump(weather_data, weather_cache, indent=4)


def get_weather_data():
    cache = __read_cache()
    if cache is not None:
        return cache["current_observation"]

    request_string = str.format("{0}{1}{2}{3}.json", endpoint_url_base, api_key, "/conditions/q/", target_city)
    response = requests.get(request_string)

    if response.status_code != 200:
        return None

    weather_data = response.json()
    __write_cache(weather_data)
    return weather_data["current_observation"]


if __name__ == "__main__":
    weather_data = get_weather_data()
    print("cached: ", __is_cache_valid(weather_data))
    print(weather_data["current_observation"]["feelslike_f"])
