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


def __parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weather",
                        action="store_true",
                        help="Suggest based on current weather.",
                        dest="use_weather")
    parser.add_argument("-m", "--multiple",
                        nargs="?",
                        help="Suggest MULTIPLE restaurants at once",
                        const=1)
    parser.add_argument("-d", "--distance",
                        action="store_true",
                        help="Look up travel time.",
                        dest="use_distance")

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


def __try_get_temperature():
    weather_data = wunderground.get_weather_data()
    if not weather_data:
        print("Trouble getting weather data. Won't be able to recommend based on weather.")
        return None
    else:
        return float(weather_data[wunderground.temperature_key])


def __try_get_travel_time(restaurant):
    travel_time = google_distance.get_travel_time(restaurant, start_address)
    if not travel_time:
        print("Trouble getting travel time.")
        return None
    else:
        return travel_time


def __get_n_suggestions(restaurants, filters, temperature, n):
    suggestions = []
    restaurants_copy = []
    restaurants_copy.extend(restaurants)
    while len(suggestions) < n:
        suggestion = suggest.suggest(restaurants_copy, filters, temperature)
        suggestions.append(suggestion)
        restaurants_copy.remove(suggestion)

    return suggestions


def __try_get_selection_at_index(index, suggested_restaurants):
    try:
        return suggested_restaurants[int(index)-1]
    except:
        print("Invalid input.")
        return None


def __generate_output_for_suggestions(suggested_restaurants, use_distance=None):
    output = []
    indexer_for_convenience = 1
    for suggested_restaurant in suggested_restaurants:
        travel_time = __try_get_travel_time(suggested_restaurant) if use_distance else None
        output.extend(output_formatting.generate_suggestion_strings(suggested_restaurant, temperature, travel_time))
        output.append(str.format("({0})", indexer_for_convenience))
        output.append("")
        indexer_for_convenience += 1

    return output


restaurant_json = file_read_write.read_json(restaurants_path)
restaurants = [Restaurant.from_dict(r) for r in restaurant_json]
arguments = __parse_args()

if not arguments.choices:
    temperature = __try_get_temperature() if arguments.use_weather else None
    suggested_restaurants = __get_n_suggestions(restaurants, arguments.filters, temperature, 3)
    if suggested_restaurants:
        output = __generate_output_for_suggestions(suggested_restaurants, arguments.use_distance)
        for line in output:
            print(line)

        selected = input("Select index of choice: (index/N)")
        selected_restaurant = __try_get_selection_at_index(selected, suggested_restaurants)\
            if selected.lower() != "n"\
            else None
        if selected_restaurant:
            selected_restaurant.last_visit = datetime.datetime.now()
            output = {"restaurants": [r for r in restaurants]}
            file_read_write.write_json(restaurants_path, output)
    else:
        print("No restaurants match the chosen filters.")
else:
    list_restaurants.list_restaurants(restaurants, arguments.choices)
