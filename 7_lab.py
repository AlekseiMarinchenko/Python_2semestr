import requests
import json
from translate import Translator

def response_analysis(response):
    if response.status_code == 200:
        print('Everything is OK!')
    else:
        print(response)


def translate_text(text):
    translator = Translator(to_lang="ru")
    translation = translator.translate(text)
    return translation


def write_json(data):
    with open(input('Ссылка на сохранение json: \n'), 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)



city = "Saint Petersburg"


def get_weather_api():
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': "5ff5ff55442ec19bd90f9334041f2cd5",
        'units': 'metric',
    }
    response = requests.get(url, params=params)

    analysis(response)
    get_useful_weather_info(response)


def get_useful_weather_info(response):
    data = response.json()
    weather_description = translate_text(data['weather'][0]['description'])
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']

    print(f"\nПогода: {weather_description}")
    print(f"Температуа: {temperature}°C")
    print(f"Влажность: {humidity}%")
    print(f"Давление: {pressure} кПа")
def main():
    funcs = {
        '1': get_weather_api,
        '0': exit
    }
    start = input('Выберите программу:\n'
                  '1: Api погоды в СПб\n'
                  '0: Выход\n')
    return funcs[start]()


if __name__ == "__main__":
    main()
