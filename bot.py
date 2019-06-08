#!/usr/bin/python

import telebot
from telebot import types
import datetime
from datetime import date
import os

# with open('bot_token.txt', 'r') as vip_file:
#     TOKEN = vip_file.read()

TOKEN = os.getenv('TOKEN', 0)

if TOKEN == 0:
    print("No token")

stickers_dict = {}
with open('stickers_id.txt', 'r') as stickers_file:
    for line in stickers_file:
        name, id = line.split(':', 2)
        stickers_dict[name] = id.strip()


bot = telebot.TeleBot(TOKEN)

date_now = date.today()
time_now = datetime.datetime.now().strftime("%H:%M:%S")
hour_now = datetime.datetime.now().hour
minute_now = datetime.datetime.now().minute

# USERS = set()
#
# src_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
# src_markup_btn1 = types.KeyboardButton('Лучшие')
# src_markup_btn2 = types.KeyboardButton('Всё подряд')
# src_markup.add(src_markup_btn1, src_markup_btn2)



@bot.message_handler(commands=['help'])
def command_handler(message):
    bot.reply_to(message, "Here all info supposed to be")

@bot.message_handler(content_types=['sticker'])
def sticker_handler(message):
    print(message.sticker)


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message,
                 'Hello, I\'m a demo reminder bot!\n'
                 'Remember that for now I\'m working only with Moscow time\n'
                 f'Moscow time is {time_now}\n'
                 f'You can set time and event ONLY for today {date_now}\n'
                 'Now give me time and name of event that you want I remind you\n'
                 'Use key-word \"set\", please'
                 )
    bot.register_next_step_handler(message, ask_time_and_event)


def ask_time_and_event(message):

    chat_id = message.chat.id
    text = message.text
    if 'set' in text:
        radz_indx = message.text.find(':')
        alarm_hour = int(''.join(c for c in message.text[:radz_indx] if c.isdigit()))
        alarm_minute = int(''.join(c for c in message.text[radz_indx:] if c.isdigit()))

        remind_msg = message.text[radz_indx+4:]

        msg_minute = '0'+str(alarm_minute) if alarm_minute < 10 else str(alarm_minute)

        bot.reply_to(message,
                     f'Ok, I will remind you {date_now} at {alarm_hour}:{msg_minute}\n'
                     f'with message \"{remind_msg}\"\n'
                     )

        while datetime.datetime.now().hour != alarm_hour:
            continue
        while datetime.datetime.now().minute != alarm_minute:
            continue
        bot.reply_to(message, remind_msg)
        bot.send_sticker(message.chat.id, stickers_dict['STICKER_UNI_DONE'])
    else:
        bot.reply_to(message, 'Please, use key-word \'set\'')


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def event_handler(message):

    text = message.text.lower()

    # if message.from_user.id in USERS:
    #     if 'hi' or 'hello' in text:
    #         reply = f"{message.from_user.first_name}, Hello again!"
    #         bot.reply_to(message, reply)
    #         bot.send_sticker(message.chat.id, stickers_dict['STICKER_BEAR_HERO'])
    # else:
    #     USERS.add(message.from_user.id)
    #     if 'hi' or 'hello' in text:
    #         bot.reply_to(message, "Hello ^_____^")
    #         bot.send_sticker(message.chat.id, stickers_dict['STICKER_KAPI_HI'])

    if 'hi' in text or 'hello' in text:
        reply = f"{message.from_user.first_name}, Hello!"
        bot.reply_to(message, reply)
        bot.send_sticker(message.chat.id, stickers_dict['STICKER_KAPI_HI'])
    elif 'bye' in text:
        reply = f"Bye, {message.from_user.first_name}! Hope to see you soon!"
        bot.reply_to(message, reply)
        bot.send_sticker(message.chat.id, stickers_dict['STICKER_AVOCADO_BYE'])
    else:
        bot.reply_to(message,
                     f"{message.from_user.first_name}, Sorry, I don\'t get it!"
                     )
        bot.send_sticker(message.chat.id, stickers_dict['STICKER_UNI_AWKWARD'])


@bot.message_handler(content_types=['photo'])
def text_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'It\'s cool')

if __name__ == '__main__':
    bot.polling(none_stop=True)