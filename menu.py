import dict as d
import handlers
from telebot import types


def button_back(message):
    handlers.bot.clear_step_handler(message)
    handlers.start_event(message)


def create_menu(lam) -> types.ReplyKeyboardMarkup:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    items = dict(filter(lam, d.BUTTONS.items()))
    for i in items.values():
        btn = types.KeyboardButton(i)
        markup.add(btn)
    return markup
