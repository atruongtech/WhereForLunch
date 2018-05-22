from data_enums import Weather, Genre
from datetime import datetime

datetime_format = "%d%m%y"


class Restaurant:
    def __init__(self, name, weather, genre_list, time, distance, last_visit, address):
        self.name = name
        self.weather = weather
        self.genre_list = genre_list
        self.time = time
        self.distance = distance
        self.last_visit = last_visit
        self.address = address

    @classmethod
    def from_dict(cls, dict_obj):
        return cls(
            dict_obj["name"],
            Weather[dict_obj["weather"]],
            [Genre[g] for g in dict_obj["genre"]],
            dict_obj["time"],
            dict_obj["distance"],
            datetime.strptime(dict_obj["last_visit"], datetime_format) if dict_obj["last_visit"] is not None else None,
            dict_obj["address"])

    def json_formattable(self):
        temp_dict = {
            "name": self.name,
            "weather": self.weather.name,
            "genre": [g.name for g in self.genre_list],
            "time": self.time,
            "distance": self.distance,
            "last_visit": datetime.strftime(self.last_visit, datetime_format) if self.last_visit is not None else None,
            "address": self.address
        }
        return temp_dict
