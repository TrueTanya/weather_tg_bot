import requests
import datetime

from requests.models import HTTPError
from config import TOKEN_WEATHER

code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

def get_uv(latitude, longitude, TOKEN_WEATHER):
    uv_reader = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat={latitude}&lon={longitude}&exclude=current,minutely,daily,alerts&appid={TOKEN_WEATHER}"
    )
    data = uv_reader.json()
    return data['hourly'][0]['uvi']

def get_weather(city_name, TOKEN_WEATHER): 
    try:
        weather_reader = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={TOKEN_WEATHER}&units=metric"
        )
        if weather_reader.status_code != 200:
            return ('Город не найден')
        data = weather_reader.json()
    except HTTPError as ex:
        print(ex)
        return ('Ошибка связи с API')

    city = data['name']
    latitude = data['coord']['lat']
    longitude = data['coord']['lon']
    cur_uv = get_uv(latitude, longitude, TOKEN_WEATHER)
    cur_weather = data['main']['temp']
    weather_description = data["weather"][0]["main"]
    if weather_description in code_to_smile:
        wd = code_to_smile[weather_description]
    else:
        wd = " "    
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind = data['wind']['speed']
    sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
    sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])

    result = (f"***{ datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
            f"Ощущается как: {feels_like}C°\n"        
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
            f"УФ-индекс: {cur_uv}\n"
            f"Восход солнца: {sunrise_timestamp} \nЗакат солнца: {sunset_timestamp}\n"
            f"Всего хорошего!")
    
    return result

def main():
    city = input("Введите город: ")
    print(get_weather(city, TOKEN_WEATHER))

if __name__ == '__main__':
    main()