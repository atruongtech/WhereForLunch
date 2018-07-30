def generate_suggestion_strings(selected_restaurant, temperature, travel_time):
    statements = [str.format("Since it feels like {0}F outside", temperature),
                  str.format("You should go to: {0}", selected_restaurant.name),
                  str.format("It has a time factor of {0}", selected_restaurant.time),
                  str.format("You last visited {0}", selected_restaurant.last_visit.strftime("%A, %m/%d/%y"))
                  if selected_restaurant.last_visit is not None
                  else "You have never been!"]

    if temperature is None:
        statements = statements[1:]
    if travel_time:
        statements.append(str.format("it will take {0} to get there", travel_time))

    return statements
