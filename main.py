from Browse import list_restaurants
from Configuration.whereforlunch_config import restaurants_path
from data_enums import Genre
from restaurant import Restaurant
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


restaurant_json = file_read_write.read_json(restaurants_path)
restaurants = [Restaurant.from_dict(r) for r in restaurant_json]
arguments = parse_args()
if arguments.choices is None:
    arguments.suggest_strategy(restaurants, arguments.filter)
else:
    list_restaurants.list_restaurants(restaurants, arguments.choices)
