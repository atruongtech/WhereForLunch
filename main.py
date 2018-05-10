from data_enums import Weather, Genre
from restaurant import Restaurant
import file_read_write
import datetime
import random
import wunderground

restaurant_json = file_read_write.read_json("./Configuration/user_restaurants.json")
restaurants = [Restaurant.from_dict(r) for r in restaurant_json]

weather_data = wunderground.get_weather_data()
eligible_restaurants = [r for r in restaurants if r.weather == Weather.cold] \
    if float(weather_data[wunderground.temperature_key]) < 72 \
    else restaurants

accepted = None
while accepted is None or accepted.lower() != "y":
    selected_restaurant = eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
    weather_statement = str.format("Since it feels like {0}F outside", weather_data[wunderground.temperature_key])
    restaurant_choice_statement = str.format("You should go to: {0}", selected_restaurant.name)
    time_statement = str.format("It has a time factor of {0}", selected_restaurant.time)
    distance_statement = str.format("and a distance factor of {0}", selected_restaurant.distance)
    last_visit_statement = str.format("You last visited {0}", selected_restaurant.last_visit) \
        if selected_restaurant.last_visit is not None \
        else "You have never been!"

    print(weather_statement)
    print(restaurant_choice_statement)
    print(time_statement)
    print(distance_statement)
    print(last_visit_statement)
    accepted = input("Are you going to go here? (Y/N)\n")
else:
    selected_restaurant.last_visit = datetime.datetime.now()
    output = {"restaurants": [r for r in restaurants]}
    file_read_write.write_json("./Configuration/user_restaurants.json", output)