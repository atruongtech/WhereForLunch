from data_enums import Weather, Genre
from restaurant import Restaurant
from Configuration.whereforlunch_config import restaurants_path
import argparse
import file_read_write
import datetime
import output_formatting
import random
import wunderground


def parse_args():
    parser = argparse.ArgumentParser()
    arg_group = parser.add_mutually_exclusive_group(required=False)
    arg_group.add_argument("--choices", "-c",
                           nargs="?",
                           help="See choices and optionally filter by genre.",
                           choices=[g.name for g in Genre],
                           const=[])
    arg_group.add_argument("--filter", "-f",
                           nargs="?",
                           help="Only suggest from the specified genres",
                           choices=[g.name for g in Genre],
                           const=[])
    return parser.parse_args()


def suggest_based_on_temp():
    restaurant_json = file_read_write.read_json(restaurants_path)
    restaurants = [Restaurant.from_dict(r) for r in restaurant_json]
    weather_data = wunderground.get_weather_data()
    if weather_data is None:
        print("Trouble getting weather data. Won't be able to recommend based on weather.")
    eligible_restaurants = [r for r in restaurants if r.weather == Weather.cold] \
        if weather_data is not None and float(weather_data[wunderground.temperature_key]) < 72 \
        else restaurants

    accepted = None
    while accepted is None or accepted.lower() != "y":
        if accepted is not None and accepted.lower() == "quit":
            break

        selected_restaurant = eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
        suggestion_statements = output_formatting.generate_suggestion_strings(selected_restaurant,
                                                                              weather_data[
                                                                                  wunderground.temperature_key])
        for statement in suggestion_statements:
            print(statement)

        accepted = input("Are you going to go here? (Y/N/quit)\n")
    else:
        selected_restaurant.last_visit = datetime.datetime.now()
        output = {"restaurants": [r for r in restaurants]}
        file_read_write.write_json(restaurants_path, output)


def list_restaurants(genre):
    restaurant_json = file_read_write.read_json(restaurants_path)
    restaurants = [Restaurant.from_dict(r) for r in restaurant_json]

    if genre:
        genre_enum = Genre[genre]
        filtered_restaurants = [r for r in restaurants if genre_enum in r.genre_list]
        for r in filtered_restaurants:
            print(r.name)
    else:
        for r in restaurants:
            print(r.name)


arguments = parse_args()
if arguments.choices is None:
    suggest_based_on_temp()
else:
    list_restaurants(arguments.choices)
