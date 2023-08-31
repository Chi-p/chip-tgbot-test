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
            menu.button_back(message)
        elif message.text in d.BUTTONS.values():
            mes = bot.send_message(
                message.from_user.id,
                d.ANSWERS[message.text],
                reply_markup=menu.create_menu(lambda x: x[0] == 'back'))
            if message.text == d.BUTTONS['message_to_audio']:
                bot.register_next_step_handler(mes, actions.message_to_audio)
        elif message.text == 'unknown messages':
            actions.read_file()
            bot.send_message(message.from_user.id, d.ANSWERS[message.text] + ', '.join(config.UNKNOWN_MESSAGES))
        elif message.text == 'clear unknown messages':
            actions.clear_unknown_messages()
            bot.send_message(message.from_user.id, d.ANSWERS[message.text])
        else:
            bot.send_message(message.from_user.id, d.ANSWERS[message.text])
    except KeyError:
        bot.send_message(message.from_user.id, d.ANSWERS['unknown'])
        actions.save_unknown_messages(message.text)
