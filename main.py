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
if float(weather_data["current_observation"]["feelslike_f"]) < 72:
    eligible_restaurants = [r for r in restaurants if r.weather == Weather.cold]
else:
    eligible_restaurants = restaurants

selected_restaurant = eligible_restaurants[random.randint(0, len(eligible_restaurants) - 1)]
print(str.format("Since it feels like {0}F outside", weather_data["current_observation"]["feelslike_f"]))
print("You should go to: ", selected_restaurant.name)
print("It has a time factor of ", selected_restaurant.time)
print("and a distance factor of", selected_restaurant.distance)
