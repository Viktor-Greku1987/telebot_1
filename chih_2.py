import telebot
from telebot import types, TeleBot
import random
import requests
appid = 'ecf8f7c99b22ef5a327aa9d6f296cc4c'
# создаем обем объект бибилиотеки телебот и с помощью токин кода соединяеемся со своим ботом
bot: TeleBot = telebot.TeleBot("5362635269:AAG7ujmsddQeH3pupqWx1Wki0ubZKPvhQQU")
# функция обработки сообщений бота
# к функции добавим декоратор (анатоции ) которая указывает с каким видлм сообщений будем работать
name = str()  # переменная для храненяия имени пользователя
surname = str()  # перемененая для храниения фамилии пользователя
age = 0  # переменная для храненич возраста пользователя
answer1 =str()


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # список различных приветсвий
    # List_utro = ['доброе утро, "хорошего Вам утра", "утро доброе"]
    # List_day = ['доброе день, "хорошего Вам дня", "доброго дня"]
    # List_evening = ['доброе вечер, "хорошего Вам вечера"]
    # List_night = ['доброй ночи']
    list_hallo = ['привет', 'добрый день', 'hello', 'добрый вечер', 'доброй ночи', 'доброй ночи']
    list_Poka = ['досвидания', 'всего хорошего', 'Goodbye', 'пока', 'поки', 'удачи', 'спокойной ночи', 'прощайте',
                 'счастливо']
    if message.text.lower() in list_hallo:
        poz = random.randint(0, len(list_hallo) - 1)
        # возвращаем сообщение в чат как ответ бота
        bot.send_message(message.from_user.id, list_hallo[poz])
        bot.send_message(message.from_user.id, ' как твое имя?')
        bot.register_next_step_handler(message, get_name)
    elif message.text.lower() in list_Poka:
        pok = random.randint(0, len(list_Poka) - 1)
        bot.send_message(message.from_user.id, list_Poka[pok])
        # возвращаем сообщение в чат как ответ бота - прощание!
   # elif message.text == '/reg':
     #   bot.send_message(message.from_user.id, ' как твое имя')
        # # get_name - это функция следующего шага, от пользователя получаем имя и вызываем ф-цю для полукчения фамилии
    #    bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'подумай еще')


def get_name(message):
    global name;
    name = message.text  # зписали имя пользователя
    bot.send_message(message.from_user.id, ' Какая ваша фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname;
    surname = message.text
    #bot.send_message(message.from_user.id, ' хотите узнать прогноз погодв?')
    bot.register_next_step_handler(message, get_text_messages)

      # создадим клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    # создадим кнопку "Да"
    key_yes = types.InlineKeyboardButton(text='ПОДТВЕРЖДАЮ', callback_data='yes')
    # добавим кнопку " да " в клавиатуру
    keyboard.add(key_yes)

    # создадим кнопку "нет"
    key_no = types.InlineKeyboardButton(text='нет', callback_data='no')
    # добавим кнопку " нет " в клавиатуру
    keyboard.add(key_no)
    global answer1;
    answer = 'тебя зовут ' + name + " " + surname +"?"
    answer1 = name + " " + surname
    # когда от пользователя получим всю инфу выведем сообщенгие для подтверждения
    bot.send_message(message.from_user.id, text=answer, reply_markup = keyboard)


    # создадим функцию обработки нажатия кнопок
@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, ' получай, ')
    elif call.data == "no":
        # реализуем логику длы нового запроса данных
        bot.send_message(call.message.chat.id, ' красавчик')



@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        # можно реализовать различную логику по сохранению данн пользователя
        bot.send_message(call.message.chat.id, ' ваши данные сохранены, ')

        # создадим клавиатуру
        keyboard = types.InlineKeyboardMarkup()
        # создадим кнопку "Да"
        key_yes = types.InlineKeyboardButton(text='ПОДТВЕРЖДАЮ', callback_data='yes')
        # добавим кнопку " да " в клавиатуру
        keyboard.add(key_yes)

        # создадим кнопку "нет"
        key_no = types.InlineKeyboardButton(text='нет', callback_data='no')
        # добавим кнопку " нет " в клавиатуру
        keyboard.add(key_no)
        bot.send_message(call.message.chat.id, 'хотите узнать прогноз погоды в Москве?', reply_markup=keyboard)
       # bot.register_next_step_handler(call.message.chat.id, callback)
    elif call.data == "no":
        # реализуем логику длы нового запроса данных
        bot.send_message(call.message.chat.id, ' огорчительно')





@bot.message_handler(content_types=['text'])
def get_text_messages(message):
   # List_utro = ['доброе утро, "хорошего Вам утра", "утро доброе"]
    if message.text == "/start" or message.text.lower() == "погода" or message.text.lower() == "да" :
        result = answer1+',' + ' в городе Москва сегодня погода: '
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

#  bot.send_message(message.from_user.id, '  Сколько Вам лет?')
#  bot.register_next_step_handler(message, get_age)

'''  


def get_text_messages_poka(message_pok):
    # список различных приветсвий
    list_pok = ['Пока-пока','И Вам всего доброго', 'рад был пообщаться', 'спасибо за уделонное время. Всего наилучшего!']

    if message_pok.text == 'Пока' or 'Дозавтра'or 'До завтра' or 'всего хорошего' or 'Всего хорошего' or 'Досвидания' or 'досвидания':
        poz = random.randint(0, len(list_pok)-1)
        # возвращаем сообщение в чат как ответ бота
        bot.send_message(message_pok.from_user.id, list_pok[poz])
    else:
        bot.send_message(message_pok.from_user.id, 'моя твоя не понимать')
        '''
# следующая команда настраивает прослушивание сервера телеграмм
bot.polling(none_stop=True, interval=0)
