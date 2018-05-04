from data_enums import weather_map, genre_map


class Restaurant:
    def __init__(self, name, weather, genre, time, distance):
        self.name = name
        self.weather = weather
        self.genre = genre
        self.time = time
        self.distance = distance

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            dict_obj["name"],
            weather_map[dict_obj["weather"]],
            genre_map[dict_obj["genre"]],
            dict_obj["time"],
            dict_obj["distance"])

    def json_formattable(self):
        temp_dict = {
            "name": self.name,
            "weather": self.weather.name,
            "genre": self.genre.name,
            "time": self.time,
            "distance": self.distance
        }
        return temp_dict
