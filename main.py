import telebot
from telebot import types, TeleBot
import random
import sqlite3

# создаем обем объект бибилиотеки телебот и с помощью токин кода соединяеемся со своим ботом
bot: TeleBot = telebot.TeleBot("5362635269:AAG7ujmsddQeH3pupqWx1Wki0ubZKPvhQQU")
# функция обработки сообщений бота
# к функции добавим декоратор (анатоции ) которая указывает с каким видлм сообщений будем работать
name = str()  # переменная для храненяия имени пользователя
surname = str()  # перемененая для храниения фамилии пользователя
age = 0  # переменная для храненич возраста пользователя
id_user = 0

# функция записывает в базу данных данные пользователя
def input_data(id, name, surname, age):
    print(id_user, name, surname, age)
    # подключаемся с созданной базой данных в програме sql3
    con = sqlite3.connect('user_tele.db')
    # создаем обем обект - курсор для взаимодействия с базой данных
    cur = con.cursor()
    # из исходных данных созданим кортеж для безопасного добаленич информаци в базу через запрос
    data = (id, name, surname, age)
    print(data)
    #  в виде строки создадим запрос для добадения данных в базу
    sql = 'insert into user (id, name, surname, age) values (?, ?, ?, ?)'
    # выполняем запрос в базу данных
    cur.execute(sql, data)
    # подтверждаем транзакцию для сохранинеия данных
    con.commit()
    cur.close()
    con.close()
# функциячя на вход принимает ID пользователя и возвращаетего имя или пустую ст року если такоего подьзователя нет в базе данных

def user_search(id):
        # подключаемся с созданной базой данных в програме sql3
    con = sqlite3.connect('user_tele.db')
    # создаем обем обект - курсор для взаимодействия с базой данных
    cur = con.cursor()

    data = (id,)
    # виды строки для поиса пользователя по ID пользователя в базе данных
    sql = 'select * from user where id=?'
    # выполняем запрос в базу данных
    cur.execute(sql, data)
    name = ""
    surname = ''

    #  спомощь цикла fор пройдемся по всем данным , которые получили из базы
    for vaue in cur:
        name = vaue[1]
        surname = vaue[2]
        z = name + " " + surname
    cur.close()
    con.close()

    return z

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    # список различных приветсвий
    # List_utro = ['доброе утро, "хорошего Вам утра", "утро доброе"]
    # List_day = ['доброе день, "хорошего Вам дня", "доброго дня"]
    # List_evening = ['доброе вечер, "хорошего Вам вечера"]
    # List_night = ['доброй ночи']

    user_mane = user_search(message.from_user.id)
    list_hallo = ['привет', 'добрый день', 'hello', 'добрый вечер', 'доброй ночи', 'доброй ночи']
    list_Poka = ['досвидания', 'всего хорошего', 'Goodbye', 'пока', 'поки', 'удачи', 'спокойной ночи', 'прощайте',
                 'счастливо']
    if message.text.lower() in list_hallo:
        poz = random.randint(0, len(list_hallo) - 1)
        # возвращаем сообщение в чат как ответ бота
        if user_mane == '':
            bot.send_message(message.from_user.id, list_hallo[poz])
            bot.send_message(message.from_user.id, ' как твое имя?')
            bot.register_next_step_handler(message, get_name)
        else:
            bot.send_message(message.from_user.id, list_hallo[poz]+', ' + user_mane+ '!')

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

    bot.send_message(message.from_user.id, '  Сколько Вам лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age;
    while age == 0:
        try:
            # полученный возраст пареобразуем в число
            age = int(message.text)
        except Exception:  # except-перехват исключения, Exception- перехватыввает все исключения(или все ощшибики)
            bot.send_message(message.from_user.id, 'введит возраст арабскими цифрами')
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

    answer = 'тебя зовут ' + name + " фамилия " + surname + " твой возраст " + str(age) + "?"
    global id_user;
    id_user = message.from_user.id

    # когда от пользователя получим всю инфу выведем сообщенгие для подтверждения
    bot.send_message(message.from_user.id, text=answer, reply_markup=keyboard)


    # создадим функцию обработки нажатия кнопок
@bot.callback_query_handler(func = lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        # вызывве функцию по заполению базы данных и записываем  в нее переменные
        print(id_user, name, surname, age)
        input_data(id_user, name, surname, age)
        # можно реализовать различную логику по сохранению данн пользователя
        bot.send_message(call.message.chat.id, ' ваши данные сохранены')

    elif call.data == "no":
        # реализуем логику длы нового запроса данных
        bot.send_message(call.message.chat.id, ' огорчительно')


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
