from enum import Enum


class Weather(Enum):
    undefined = 0,
    hot = 1,
    cold = 2


class Genre(Enum):
    undefined = 0,
    hotpot = 1,
    pizza = 2


weather_map = {
    "undefined": Weather.undefined,
    "cold": Weather.cold,
    "hot": Weather.hot
}
genre_map = {
    "undefined": Genre.undefined,
    "hotpot": Genre.hotpot,
    "pizza": Genre.pizza
}
