from data_enums import Weather, Genre
from restaurant import Restaurant
from Configuration.whereforlunch_config import restaurants_path
import file_read_write
import datetime
import output_formatting
import random
import wunderground

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
    selected_restaurant = eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
    suggestion_statements = output_formatting.generate_suggestion_strings(selected_restaurant,
                                                                          weather_data[wunderground.temperature_key])
    for statement in suggestion_statements:
        print(statement)

    accepted = input("Are you going to go here? (Y/N)\n")
else:
    selected_restaurant.last_visit = datetime.datetime.now()
    output = {"restaurants": [r for r in restaurants]}
    file_read_write.write_json(restaurants_path, output)
