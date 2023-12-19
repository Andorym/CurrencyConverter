import telebot  
from config import keys, TOKEN  
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)  


@bot.message_handler(commands=['start',
                               'help'])  
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате:\n <имя валюты> \
    <в какую валюту конвертировать> \
    <количество валюты>\n Увидеть список всех доступных валют /values '
    bot.reply_to(message, text)


@bot.message_handler(
    commands=['values'])  
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')  
        if len(values) != 3:
            raise APIException('Не правильное количество введенных данных! \
            \nВведите через пробел три параметра: <имя валюты> \
    <в какую валюту конвертировать> \
    <количество конвертируемой валюты>')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)  
    except APIException as e:  
        bot.reply_to(message, f'Ошибка пользователя! \n{e}')
    except Exception as e:  
        bot.reply_to(message, f'Не удалось обработать команду! \nПричина: {e}')
    else:  
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
