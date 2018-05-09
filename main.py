from data_enums import Weather, Genre
from restaurant import Restaurant
import file_read_write
import json
import random
import wunderground

restaurant_json = file_read_write.read_json("./Configuration/user_restaurants.json")
restaurants = [Restaurant.from_dict(r) for r in restaurant_json]

# new_restaurant = Restaurant(name="Jazz Cat", weather=Weather.cold, genre=Genre.hotpot, time=2, distance=3)
# if not next((i for i in restaurants if i.name == new_restaurant.name), None):
#    restaurants.append(new_restaurant)

# output = {"restaurants": [r for r in restaurants]}
# file_read_write.write_json("./Configuration/user_restaurants_temp.json", output)

weather_data = wunderground.get_weather_data()
eligible_restaurants = [r for r in restaurants if r.weather == Weather.cold] \
                        if float(weather_data[wunderground.temperature_key]) < 72  \
                        else restaurants

selected_restaurant = eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
weather_statement = str.format("Since it feels like {0}F outside", weather_data[wunderground.temperature_key])
restaurant_choice_statement = str.format("You should go to: {0}", selected_restaurant.name)
time_statement = str.format("It has a time factor of {0}", selected_restaurant.time)
distance_statement = str.format("and a distance factor of {0}", selected_restaurant.distance)
last_visit_statement = str.format("You last visited {0}", selected_restaurant.last_visit) \
                        if selected_restaurant.last_visit is not None\
                        else "You have never been!"

print(weather_statement)
print(restaurant_choice_statement)
print(time_statement)
print(distance_statement)
print(last_visit_statement)
