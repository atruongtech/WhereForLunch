from Browse import list_restaurants
from Configuration.whereforlunch_config import restaurants_path, start_address
from data_enums import Genre
from restaurant import Restaurant
from Suggest import suggest
import argparse
import datetime
import google_distance
import file_read_write
import output_formatting
import wunderground


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weather",
                        action="store_true",
                        dest="use_weather")

    arg_group = parser.add_mutually_exclusive_group(required=False)
    arg_group.add_argument("-c", "--choices",
                           nargs="?",
                           help="See choices and optionally filter by genre.",
                           choices=[g.name for g in Genre],
                           const=[])
    arg_group.add_argument("-f", "--filters",
                           nargs="+",
                           help="Only suggest from the specified genres",
                           choices=[g.name for g in Genre])
    return parser.parse_args()


def get_temperature():
    weather_data = wunderground.get_weather_data()
    if not weather_data:
        print("Trouble getting weather data. Won't be able to recommend based on weather.")
        return None
    else:
        return float(weather_data[wunderground.temperature_key])


def get_travel_time(restaurant):
    travel_time = google_distance.get_travel_time(restaurant, start_address)
    if not travel_time:
        print("Trouble getting travel time.")
        return None
    else:
        return travel_time


restaurant_json = file_read_write.read_json(restaurants_path)
restaurants = [Restaurant.from_dict(r) for r in restaurant_json]
arguments = parse_args()

if arguments.choices is None:
    temperature = get_temperature() if arguments.use_weather else None
    suggested_restaurant = suggest.suggest(restaurants, arguments.filters, temperature)
    travel_time = get_travel_time(suggested_restaurant)
    if suggested_restaurant:
        output = output_formatting.generate_suggestion_strings(suggested_restaurant, temperature, travel_time)
        for line in output:
            print(line)
        accepted = input("Are you going to go here? (Y/N)")
        if accepted.lower() == "y":
            suggested_restaurant.last_visit = datetime.datetime.now()
            output = {"restaurants": [r for r in restaurants]}
            file_read_write.write_json(restaurants_path, output)
    else:
        print("No restaurants match the chosen filters.")
else:
    list_restaurants.list_restaurants(restaurants, arguments.choices)
