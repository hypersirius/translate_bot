from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from configs import LANGUAGES



def generate_language():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = []

    for language in LANGUAGES.values():
        btn = KeyboardButton(text=language)
        buttons.append(btn)

    markup.add(*buttons)
    return markup

def generate_back():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = KeyboardButton(text='Назад')
    markup.add(btn)
    return markup
