import telebot
import requests
import json
from config import keys, TOKEN
from extensions import APIException, Curr_Exchange

# TOKEN = ""
bot = telebot.TeleBot(TOKEN)

# keys = {
#     'доллар': 'USD',
#     'евро': 'EUR',
#     'рубль': 'RUB'
# }

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! \nЯ бот-помощник по обмену валюты. Для начала работы введи команду в следующем формате (через пробел):' \
           '\n- <Название валюты, которую ты хочешь обменять>  ' \
           '\n- <Название валюты, на которую ты хочешь обменять свою валюту> ' \
           '\n- <Количество первой валюты (например, 50.00)>\n \
 Список доступных валют: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)



# base, quote, amount = message.text.split(' ')
@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException('Введено параметров больше, чем нужно. Попробуем еще раз?')

        if len(values) < 3:
            raise APIException('Введены не все параметры. Попробуем еще раз?')

        base, quote, amount = values
        total_base = Curr_Exchange.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя :( \n{e}')

    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так... :(\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote}: {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
