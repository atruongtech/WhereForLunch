import json


def read_json(path):
    with open(path, "r") as read_file:
        restaurants_container = json.load(read_file)
        return restaurants_container["restaurants"]


def write_json(path, output):
    with open(path, "w") as write_file:
        json.dump(output, write_file, default=lambda o: o.json_formattable(), indent=4, sort_keys=True)
