import telebot
from telebot import types, TeleBot
import requests
import random
# указать полученый API-ключ отсайта
appid = 'ecf8f7c99b22ef5a327aa9d6f296cc4c'
# создаем обем объект бибилиотеки телебот и с помощью токин кода соединяеемся со своим ботом
bot: TeleBot = telebot.TeleBot("5362635269:AAG7ujmsddQeH3pupqWx1Wki0ubZKPvhQQU")
# функция обработки сообщений бота
# к функции добавим декоратор (анатоции ) которая указывает с каким видлм сообщений будем работать


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start" or message.text.lower() == "погода" :
        result = ' В городе Москва се6годня погода: '
        city_id = search_City_Id()
        result += weather_current_day(city_id)
        bot.send_message(message.from_user.id, result)
    else:
        bot.send_message(message.from_user.id, 'для получения погоды введите слово "Погода"')
# функция по указанному городу и стране находит ID  города в базе сервера (по умолчению г. Москва)
def search_City_Id(s_city = 'Moscow,RU'):
    city_id = 0
    # проверка на существование грода и его ID
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/find', params = {'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
        data = res.json()


        city_id = data['list'][0]['id']

    except Exception as e:
        city_id = -1
    return city_id
# функция выдает погоду на текущий день по укащзанному городу
def weather_current_day(city_id):
    result = ''
    try:
        res = requests.get('http://api.openweathermap.org/data/2.5/weather', params = {'id': city_id, 'units': 'metric', 'long': 'ru', 'APPID': appid})
        data = res.json()

        result += ' температура: ' + str(data['main']['temp'])
        result += ' максимальная температура: ' + str(data['main']['temp_max'])
        result += ' минммальная температура :' + str(data['main']['temp_min'])
        result += ' осодки :' +  str(data['weather'][0]['description'])
    except Exception as e:
        result = ''
    return result
# следующая команда настраивает прослушивание сервера телеграмм
bot.polling(none_stop=True, interval=0)
