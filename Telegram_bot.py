import telebot  
from config import keys, TOKEN  
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)  


@bot.message_handler(commands=['start',
                               'help'])  
def help(message: telebot.types.Message):
    text = '����� ������ ������ ������� ������� ���� � �������:\n <��� ������> \
    <� ����� ������ ��������������> \
    <���������� ������>\n ������� ������ ���� ��������� ����� /values '
    bot.reply_to(message, text)


@bot.message_handler(
    commands=['values'])  
def values(message: telebot.types.Message):
    text = '��������� ������'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')  
        if len(values) != 3:
            raise APIException('�� ���������� ���������� ��������� ������! \
            \n������� ����� ������ ��� ���������: <��� ������> \
    <� ����� ������ ��������������> \
    <���������� �������������� ������>')
        quote, base, amount = values
        total_base = CurrencyConverter.get_price(quote, base, amount)  
    except APIException as e:  
        bot.reply_to(message, f'������ ������������! \n{e}')
    except Exception as e:  
        bot.reply_to(message, f'�� ������� ���������� �������! \n�������: {e}')
    else:  
        text = f'���� {amount} {quote} � {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
