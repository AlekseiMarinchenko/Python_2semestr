import json
import requests
import speech_recognition as sr
from currencies import print_currencies

currencies_list = {
        'австралийский доллар': 'AUD',
        'азербайджанский манат': 'AZN',
        'фунт стерлингов': 'GBP',
        'армянский драм': 'AMD',
        'белорусский рубль': 'BYN',
        'болгарский лев': 'BGN',
        'бразильский реал': 'BRL',
        'венгерский форинт': 'HUF',
        'вьетнамский донг': 'VND',
        'гонконгский доллар': 'HKD',
        'грузинский лари': 'GEL',
        'датская крона': 'DKK',
        'дирхам ОАЭ': 'AED',
        'американский доллар': 'USD',
        'евро': 'EUR',
        'египетский фунт': 'EGP',
        'индийская рупия': 'INR',
        'индонезийская рупия': 'IDR',
        'казахстанский тенге': 'KZT',
        'канадский доллар': 'CAD',
        'катарский риал': 'QAR',
        'киргизский сом': 'KGS',
        'китайский юань': 'CNY',
        'молдавский лей': 'MDL',
        'новозеландский доллар': 'NZD',
        'норвежская крона': 'NOK',
        'польский злотый': 'PLN',
        'румынский лей': 'RON',
        'специальные права заимствования': 'XDR',
        'сингапурский доллар': 'SGD',
        'таджикский сомони': 'TJS',
        'таиландский бат': 'THB',
        'турецкая лира': 'TRY',
        'туркменский манат': 'TMT',
        'узбекский сум': 'UZS',
        'украинская гривна': 'UAH',
        'чешская крона': 'CZK',
        'шведская крона': 'SEK',
        'швейцарский франк': 'CHF',
        'сербский динар': 'RSD',
        'южноафриканский рэнд': 'ZAR',
        'южнокорейская вона': 'KRW',
        'японская иена': 'JPY'
    }


def convert_currency_request(text):
    text = text.lower()
    for item in currencies_list:
        if text in item:
            return currencies_list[item]
    return 'Fail'


def print_currencies():
    currency_names = list(currencies_list.keys())
    for i in range(0, len(currency_names), 5):
        print(" | ".join(currency_names[i:i + 5]))


def check_the_currency(currency, data_cur):
    if currency == 'Fail':
        print('Такой валюты нет...')
        exit()
    value = round(1 / float(data_cur["rates"][currency]), 2)
    date = data_cur["date"]
    currency_name = next((name for name, code in currencies_list.items() if code == currency), '???')
    print(f'На момент {date}\n1 {currency}({currency_name}) = {value} RUB(рубль)')


def get_api():
    url = "https://www.cbr-xml-daily.ru/latest.js"
    response = requests.get(url)
    response_analysis(response)
    return response


def response_analysis(response):
    if response.status_code != 200:
        print(response)


def get_info_from_response(response):
    data = json.loads(response.text)
    return data


def recognize_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Назовите валюту из списка: ")
        print_currencies()

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source, timeout=3)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            print("Вывод валюты: " + text + '\n')
            return text
        except sr.UnknownValueError:
            print("Речь не распознана.")
            return 'Fail'
          
def currency_voice_assistant():
    text = recognize_text()
    if text == 'Fail':
        print('Ошибка!!!')
        return 1

    response = get_api()

    data_cur = get_info_from_response(response)

    currency = convert_currency_request(text)

    check_the_currency(currency, data_cur)
  
def main():
    funcs = {
        '1': currency_voice_assistant,
        '0': exit
    }
    start = input('Выберите программу:\n'
                  '1: Запустить голосового помощника\n'
                  '0: Выход\n')
    return funcs[start]()


if __name__ == "__main__":
    main()
