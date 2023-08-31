import file
import telebot
import menu
import actions
import config
import dict as d

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start_event(message):
    bot.send_message(
        message.from_user.id,
        d.ANSWERS['start'],
        reply_markup=menu.create_menu(lambda x: x[0] != 'back'))


@bot.message_handler(content_types=['text'])
def send_message(message):
    try:
        if message.text == d.BUTTONS['back']:
            bot.clear_step_handler(message)
            start_event(message)
        elif message.text in d.BUTTONS.values() and message.text != d.BUTTONS['back']:
            mes = bot.send_message(
                message.from_user.id,
                d.ANSWERS[message.text],
                reply_markup=menu.create_menu(lambda x: x[0] == 'back'))
            if message.text == 'Текст в аудио':
                bot.register_next_step_handler(mes, actions.message_to_audio)
        elif message.text == 'unknown messages':
            file.read_file(config.UNKNOWN_MESSAGES_FILENAME)
            bot.send_message(message.from_user.id, ', '.join(config.UNKNOWN_MESSAGES))
        else:
            bot.send_message(message.from_user.id, d.ANSWERS[message.text])
    except KeyError:
        bot.send_message(message.from_user.id, d.ANSWERS['unknown'])
        file.save_unknown_messages(message.text)
