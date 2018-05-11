
def generate_suggestion_strings(selected_restaurant, temperature):
    statements = [str.format("Since it feels like {0}F outside", temperature),
                  str.format("You should go to: {0}", selected_restaurant.name),
                  str.format("It has a time factor of {0}", selected_restaurant.time),
                  str.format("and a distance factor of {0}", selected_restaurant.distance),
                  str.format("You last visited {0}", selected_restaurant.last_visit)
                              if selected_restaurant.last_visit is not None
                              else "You have never been!"]

    return statements
