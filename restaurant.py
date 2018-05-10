from data_enums import weather_map, genre_map
from datetime import datetime

datetime_format = "%d%m%y"


class Restaurant:
    def __init__(self, name, weather, genre, time, distance, last_visit):
        self.name = name
        self.weather = weather
        self.genre = genre
        self.time = time
        self.distance = distance
        self.last_visit = last_visit

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            dict_obj["name"],
            weather_map[dict_obj["weather"]],
            genre_map[dict_obj["genre"]],
            dict_obj["time"],
            dict_obj["distance"],
            datetime.strptime(dict_obj["last_visit"], datetime_format) if dict_obj["last_visit"] is not None else None)

    def json_formattable(self):
        temp_dict = {
            "name": self.name,
            "weather": self.weather.name,
            "genre": self.genre.name,
            "time": self.time,
            "distance": self.distance,
            "last_visit": datetime.strftime(self.last_visit, datetime_format) if self.last_visit is not None else None
        }
        return temp_dict
