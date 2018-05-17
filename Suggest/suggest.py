import file_read_write
import output_formatting
import wunderground
from Configuration.whereforlunch_config import restaurants_path
from data_enums import Weather, Genre
from restaurant import Restaurant

import random
from datetime import datetime


def suggest_based_on_temp(genre_filters=None):
    weather_data = wunderground.get_weather_data()
    if weather_data is None:
        print("Trouble getting weather data. Won't be able to recommend based on weather.")
        return suggest(genre_filters)
    else:
        temperature = float(weather_data[wunderground.temperature_key])
        return suggest(genre_filters, temperature)


def suggest(genre_filters=None, temperature=None):
    restaurant_json = file_read_write.read_json(restaurants_path)
    restaurants = [Restaurant.from_dict(r) for r in restaurant_json]

    eligible_restaurants = __filter_weather(restaurants, temperature)
    eligible_restaurants = __filter_genre(genre_filters, eligible_restaurants)
    if not eligible_restaurants:
        print("No restaurants match the requested filters.")
        return

    accepted = ''
    while accepted.lower() != "y":
        if accepted.lower() == "quit":
            break

        selected_restaurant = __choose_and_present(eligible_restaurants, temperature)
        accepted = input("Are you going to go here? (Y/N/quit)\n")
    else:
        selected_restaurant.last_visit = datetime.datetime.now()
        output = {"restaurants": [r for r in restaurants]}
        file_read_write.write_json(restaurants_path, output)


def __filter_weather(restaurants, temperature):
    return [r for r in restaurants if r.weather == Weather.cold] \
        if temperature is not None and float(temperature) < 72 \
        else restaurants


def __choose_and_present(eligible_restaurants, temperature):
    selected_restaurant = eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
    suggestion_statements = output_formatting.generate_suggestion_strings(selected_restaurant, temperature)
    for statement in suggestion_statements:
        print(statement)
    return selected_restaurant


def __filter_genre(filter_strings, restaurants):
    if filter_strings:
        for f in filter_strings:
            restaurants = [r for r in filter(lambda r: Genre[f] in r.genre_list, restaurants)]

    return restaurants


if __name__ == "__main__":
    restaurants_path = "../Configuration/user_restaurants.json"
    suggest(["noodles"])
