from data_enums import Weather, Genre
import random


def suggest(restaurants, genre_filters=None, temperature=None):
    eligible_restaurants = __filter_weather(restaurants, temperature)
    eligible_restaurants = __filter_genre(eligible_restaurants, genre_filters)

    if eligible_restaurants:
        return eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
    else:
        return None


def __filter_weather(restaurants, temperature):
    return [r for r in restaurants if r.weather == Weather.cold] \
        if temperature is not None and float(temperature) < 72 \
        else restaurants


def __filter_genre(restaurants, filter_strings):
    filtered_restaurants = []
    if filter_strings:
        for f in filter_strings:
            filtered_restaurants.extend(r for r in filter(lambda r: Genre[f] in r.genre_list, restaurants))
        return filtered_restaurants
    else:
        return restaurants


if __name__ == "__main__":
    restaurants_path = "../Configuration/user_restaurants.json"
    suggest(["noodles"])
