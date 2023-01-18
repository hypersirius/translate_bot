import telebot
from googletrans import Translator
from keyboards import generate_language, generate_back
from configs import get_key, LANGUAGES
import sqlite3

TOKEN = '5433879505:AAEFhq75gSvL-MfdPzQTL3vqfQFDcB6J1N8'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', 'history'])
def start(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name else ''
    if message.text == '/start':
        bot.send_message(chat_id, f'''Привет {first_name} {last_name}.
    Я телеграм бот переводчик. Помогу тебе перевести слова и текста 😉😁''')
        start_translate(message)
        # bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEFgopi8h3koxFzrbqyG0SCJHGS0AwPiAACFg4AAi_AIEl3vjnIA6NjwikE')
    elif message.text == '/help':
        bot.send_message(chat_id, f'''Этот бот разрабатываля в учебных целях в учебном центре PROWEB.
При создании этого бота никто из учеников не пострадал. Этот разрабатывался разработчиком
https://t.me/yakhyayeff_13''', reply_markup=generate_back())
        # bot.send_sticker(chat_id, 'CAACAgIAAxkBAAEFgzpi8nsF193870v6sxHG7782pQUe2gAC6xQAAgthIEmm4YYOfjs9jCkE')
    elif message.text == '/history':
        return_history(message)


def return_history(message):
    chat_id = message.chat.id

    database = sqlite3.connect('translator.db')
    cursor = database.cursor()

    cursor.execute('''
SELECT from_lang, to_lang, original_text, translated_text
FROM history
WHERE telegram_id = ?    
''', (chat_id, ))

    history = cursor.fetchall()
    print(history)
    history = history[::-1]
    i = 0
    text = ''
    for from_lang, to_lang, org_text, tr_text in history[:5]:
        i += 1
        text += f'''{i}. Вы перевели
С языка: {from_lang}
На язык: {to_lang}
Текст: {org_text}
Бот перевел: {tr_text}\n'''

    bot.send_message(chat_id, text, reply_markup=generate_back())


@bot.message_handler(func=lambda message: message.text in 'Назад')
def return_back(message):
    start_translate(message)


def start_translate(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'С какого языка хотите перевести ?', reply_markup=generate_language())
    bot.register_next_step_handler(msg, second_lang)

@bot.message_handler(func=lambda message: message.text in LANGUAGES.values())
def second_lang(message):
    if message.text in ['/start', '/help', '/history']:
        start(message)
    else:
        src = message.text
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, f'На какой язык хотите перевести ?', reply_markup=generate_language())
        bot.register_next_step_handler(msg, give_me_text, src)


@bot.message_handler(func=lambda message: message.text in LANGUAGES.values())
def give_me_text(message, src):
    if message.text in ['/start', '/help', '/history']:
        start(message)
    else:
        chat_id = message.chat.id
        dest = message.text
        msg = bot.send_message(chat_id, f'Напишите свой текст который вы хотите перевести: ')
        bot.register_next_step_handler(msg, translate, src, dest)


def translate(message, src, dest):
    if message.text in ['/start', '/help', '/history']:
        start(message)
    else:
        chat_id = message.chat.id
        text = message.text
        translator = Translator()
        texttt = translator.translate(text=text, src=get_key(src), dest=get_key(dest)).pronunciation if translator.translate(text=text, src=get_key(src), dest=get_key(dest)) else ''
        print(texttt)
        tr_text = translator.translate(text=text, src=get_key(src), dest=get_key(dest)).text

        database = sqlite3.connect('translator.db')
        cursor = database.cursor()

        cursor.execute('''
    INSERT INTO history(telegram_id, from_lang, to_lang, original_text, translated_text)
    VALUES (?,?,?,?,?)
    ''', (chat_id, src, dest, text, tr_text))
        database.commit()
        database.close()
        bot.send_message(chat_id, f'''{tr_text}
    {texttt}''')
        start_translate(message)


bot.polling(none_stop=True)
