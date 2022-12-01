import telebot
from telebot import types, TeleBot
import random


bot: TeleBot = telebot.TeleBot('5837538521:AAF6zNac2rm9uEB8KlPuz-IThyHCN0CLhE8')
name = str()
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    list_hallo = ['привет', 'добрый день', 'hello', 'добрый вечер', 'доброй ночи', 'доброй ночи']

    list_poka = ['досвидания', 'всего хорошего', 'hello', 'пока', 'поки', 'удачи', 'спокойной ночи', 'прощайте', 'счастливо']
    if message.text.lower() in list_hallo:
        p = random.randint(0, len(list_hallo)-1)
        bot.send_message(message.from_user.id, list_hallo[p])
        bot.send_message(message.from_user.id, 'Как твое имя?')
        bot.send_message(message.from_user.id, get_name)
    elif message.text.lower in list_poka:
        poka = random.randint(0, len(list_poka)-1)
        bot.send_message(message.from_user.id, len(list_poka[poka]))
    else:
        bot.send_message(message.from_user.id, 'подумай еще')

'''
def get_NAME(message):
    global name;
    name = message.text
    bot.send_message(message.from_user.id, 'как твоя фамилия?')
    bot.register_next_step_handler(message, get_surname)
'''
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


bot.polling(none_stop=True, interval=0)
