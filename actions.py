import gtts
import handlers
import os.path
import config
import dict as d
from io import BytesIO


def message_to_audio(message):
    if message.content_type == 'text':
        if message.text == d.BUTTONS['back']:
            handlers.bot.clear_step_handler(message)
            handlers.start_event(message)
        else:
            voice = BytesIO()
            gtts.gTTS(message.text, lang='ru').write_to_fp(voice)
            voice.seek(0)
            mes = handlers.bot.send_voice(message.from_user.id, voice)
            handlers.bot.register_next_step_handler(mes, message_to_audio)
    else:
        mes = handlers.bot.send_message(message.from_user.id, d.ANSWERS['wrong_message'])
        handlers.bot.register_next_step_handler(mes, message_to_audio)


def save_unknown_messages(message):
    read_file()
    with open(config.UNKNOWN_MESSAGES_FILENAME, 'w', encoding='utf-16') as text_file:
        config.UNKNOWN_MESSAGES.add(message)
        for i in config.UNKNOWN_MESSAGES:
            print(i, file=text_file)
        text_file.close()


def clear_unknown_messages():
    if os.path.exists(config.UNKNOWN_MESSAGES_FILENAME):
        open(config.UNKNOWN_MESSAGES_FILENAME, 'w', encoding='utf-16').close()


def read_file():
    if os.path.exists(config.UNKNOWN_MESSAGES_FILENAME):
        with open(config.UNKNOWN_MESSAGES_FILENAME, 'r', encoding='utf-16') as text_file:
            res = []
            for i in text_file.readlines():
                res.append(i.replace('\n', ''))
            config.UNKNOWN_MESSAGES.clear()
            config.UNKNOWN_MESSAGES.update(res)
            text_file.close()
