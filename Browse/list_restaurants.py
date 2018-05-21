from data_enums import Genre


def list_restaurants(restaurants, genre_string):
    if genre_string:
        filtered_restaurants = [r for r in restaurants if Genre[genre_string] in r.genre_list]
        for r in filtered_restaurants:
            print(r.name)
    else:
        for r in restaurants:
            print(r.name)
