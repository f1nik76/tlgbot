import telebot
from extensions import Converter, ConvertExeption
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу с ботом, введите команду в формате \n <имя валюты> <во что перевести> <сумма>\n Список доступных валют /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Валюты, доступные для конвертации:'
    for i in keys.keys():
        text = '\n'.join([text, i])
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        all_values = message.text.title().split(' ')

        if len(all_values) != 3:
            raise ConvertExeption('Слишком много параметров')

        values_in, values_out, mount = all_values

        total = Converter.get_price(values_in, values_out, mount)
    except ConvertExeption as error:
        bot.reply_to(message, f'Ошибка пользователя:\n{error}')
    except Exception as error:
        bot.reply_to(message, f'Ошибка конвертера:\n{error}')
    else:
        text = f'Стоимость {mount} {values_in} равна {total} {values_out}'
        bot.reply_to(message, text)


bot.polling(none_stop=True)

