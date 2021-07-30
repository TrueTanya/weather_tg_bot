import requests
from pprint import pprint
import datetime
import uvi

from config import TOKEN_WEATHER


def get_weather(city_name, TOKEN_WEATHER): 

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        weather_reader = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={TOKEN_WEATHER}&units=metric"
        )
        data = weather_reader.json()
        #pprint(data)

        city = data['name']
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        cur_uv = uvi.get_uv(latitude, longitude, TOKEN_WEATHER)
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
        lenght_of_the_day = datetime.datetime.fromtimestamp(data['sys']['sunrise']) - datetime.datetime.fromtimestamp(data['sys']['sunset'])

        result = (f"***{ datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Ощущается как: {feels_like}C°\n"        
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"УФ-индекс: {cur_uv}\n"
              f"Восход солнца: {sunrise_timestamp} \nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {lenght_of_the_day}\n"
              f"Всего хорошего!")
        #print(result)

        return result
             
    except Exception as ex:
        print(ex)
        return ('Проверь название города')
           


def main():
    city = input("Введите город: ")
    get_weather(city, TOKEN_WEATHER)

if __name__ == '__main__':
    main()
    
