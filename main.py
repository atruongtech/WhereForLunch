from data_enums import Genre
from restaurant import Restaurant
from Configuration.whereforlunch_config import restaurants_path
from Suggest import suggest
import argparse
import file_read_write


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--weather",
                        action="store_const",
                        dest="suggest_strategy",
                        const=suggest.suggest_based_on_temp,
                        default=suggest.suggest)

    arg_group = parser.add_mutually_exclusive_group(required=False)
    arg_group.add_argument("-c", "--choices",
                           nargs="?",
                           help="See choices and optionally filter by genre.",
                           choices=[g.name for g in Genre],
                           const=[])
    arg_group.add_argument("-f", "--filter",
                           nargs="+",
                           help="Only suggest from the specified genres",
                           choices=[g.name for g in Genre])
    return parser.parse_args()


def list_restaurants(genre_string):
    restaurant_json = file_read_write.read_json(restaurants_path)
    restaurants = [Restaurant.from_dict(r) for r in restaurant_json]

    if genre_string:
        filtered_restaurants = [r for r in restaurants if Genre[genre_string] in r.genre_list]
        for r in filtered_restaurants:
            print(r.name)
    else:
        for r in restaurants:
            print(r.name)


arguments = parse_args()
if arguments.choices is None:
    arguments.suggest_strategy(arguments.filter)
else:
    list_restaurants(arguments.choices)
