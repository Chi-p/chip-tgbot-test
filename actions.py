import gtts
import handlers
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
