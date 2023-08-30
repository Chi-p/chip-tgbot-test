import telebot
import config
import dict
import os.path
import gtts
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_event(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_menu = types.KeyboardButton(dict.BUTTONS['menu'])
    btn_profile = types.KeyboardButton(dict.BUTTONS['profile'])
    btn_message_to_audio = types.KeyboardButton(dict.BUTTONS['message_to_audio'])
    markup.add(btn_menu, btn_profile, btn_message_to_audio)
    bot.send_message(message.from_user.id, dict.ANSWERS['start'], reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_message(message):
    try:
        if message.text == dict.BUTTONS['back']:
            start_event(message)
        elif message.text in dict.BUTTONS.values() and message.text != dict.BUTTONS['back']:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_back = types.KeyboardButton(dict.BUTTONS['back'])
            markup.add(btn_back)
            mes = bot.send_message(message.from_user.id, dict.ANSWERS[message.text], reply_markup=markup)
            if message.text == 'Текст в аудио':
                bot.register_next_step_handler(mes, message_to_audio)
        elif message.text == 'unknown messages':
            read_file(config.UNKNOWN_MESSAGES_FILENAME)
            bot.send_message(message.chat.id, ', '.join(config.UNKNOWN_MESSAGES))
        else:
            bot.send_message(message.chat.id, dict.ANSWERS[message.text])
    except KeyError:
        bot.send_message(message.chat.id, dict.ANSWERS['unknown'])
        save_unknown_messages(message.text)


def save_unknown_messages(message):
    read_file(config.UNKNOWN_MESSAGES_FILENAME)
    with open(config.UNKNOWN_MESSAGES_FILENAME, 'w', encoding='utf-16') as text_file:
        config.UNKNOWN_MESSAGES.add(message)
        for i in config.UNKNOWN_MESSAGES:
            print(i, file=text_file)


def read_file(file_name):
    if os.path.exists(file_name):
        with open(config.UNKNOWN_MESSAGES_FILENAME, 'r', encoding='utf-16') as text_file:
            res = []
            for i in text_file.readlines():
                res.append(i.replace('\n', ''))
            config.UNKNOWN_MESSAGES.update(res)


def message_to_audio(message):
    if message.text == dict.BUTTONS['back']:
        bot.clear_step_handler(message)
        start_event(message)
    else:
        file_name = f'{message.text}.mp3'
        gtts.gTTS(message.text, lang='ru').save(file_name)
        file = open(file_name, 'rb')
        mes = bot.send_audio(message.chat.id, file)
        file.close()
        os.remove(file_name)
        bot.register_next_step_handler(mes, message_to_audio)


def get_key_from_value(d, val):
    return [k for k, v in d.items() if v == val]


bot.polling(none_stop=True)
