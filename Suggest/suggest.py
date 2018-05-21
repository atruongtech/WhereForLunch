from Configuration.whereforlunch_config import restaurants_path
from data_enums import Weather, Genre
from datetime import datetime
import file_read_write
import output_formatting
import random
import wunderground


def suggest_based_on_temp(restaurants, genre_filters=None):
    weather_data = wunderground.get_weather_data()
    if weather_data is None:
        print("Trouble getting weather data. Won't be able to recommend based on weather.")
        return suggest(restaurants, genre_filters)
    else:
        temperature = float(weather_data[wunderground.temperature_key])
        return suggest(restaurants, genre_filters, temperature)


def suggest(restaurants, genre_filters=None, temperature=None):
    eligible_restaurants = __filter_weather(restaurants, temperature)
    eligible_restaurants = __filter_genre(eligible_restaurants, genre_filters)

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


def __filter_genre(restaurants, filter_strings):
    filtered_restaurants = []
    if filter_strings:
        for f in filter_strings:
            filtered_restaurants.extend(r for r in filter(lambda r: Genre[f] in r.genre_list, restaurants))
        return filtered_restaurants
    else:
        return restaurants


def __choose_and_present(eligible_restaurants, temperature):
    selected_restaurant = eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
    suggestion_statements = output_formatting.generate_suggestion_strings(selected_restaurant, temperature)
    for statement in suggestion_statements:
        print(statement)
    return selected_restaurant


if __name__ == "__main__":
    restaurants_path = "../Configuration/user_restaurants.json"
    suggest(["noodles"])
