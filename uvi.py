import requests
from pprint import pprint
import datetime
from config import TOKEN_WEATHER 


def get_uv(latitude, longitude, TOKEN_WEATHER):

  uv_reader = requests.get(
     f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=current,minutely,daily,alerts&appid={TOKEN_WEATHER}"
        )

  data = uv_reader.json()
  cur_uv = data['hourly'][0]['uvi']
  return cur_uv