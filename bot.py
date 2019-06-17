#!/usr/bin/python

import telebot
from telebot import types
import datetime
from datetime import date
import os
# import sys
# sys.path.insert(0, './calendar-telegram-master')

# import telegramcalendar

# with open('bot_token.txt', 'r') as vip_file:
#     TOKEN = vip_file.read()

TOKEN = os.getenv('TOKEN', 0)


if TOKEN == 0:
    print("No token at all")

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
                 )
    bot.send_message(message.chat.id, "Enter the time in format hour:minutes, please")

    bot.register_next_step_handler(message, ask_time)


alarm_hour = 0
alarm_minute = 0

def ask_time(message):
    global alarm_hour
    global alarm_minute
    radz_indx = message.text.find(':')
    alarm_hour = int(''.join(c for c in message.text[:radz_indx] if c.isdigit()))
    alarm_minute = int(''.join(c for c in message.text[radz_indx:] if c.isdigit()))

    bot.send_message(message.chat.id, "Enter the name of event, please")

    bot.register_next_step_handler(message, ask_event)

event = ''

def ask_event(message):
    global event

    event = message.text


    text_hour = alarm_hour if alarm_hour > 9 else "0" + str(alarm_hour)
    text_minutes = alarm_minute if alarm_minute > 9 else "0" + str(alarm_minute)

    bot.send_message(message.chat.id, f"I will remind you at {text_hour}:{text_minutes} about \"{event}\"")

    # dump way to remind >___<
    while datetime.datetime.now().hour != alarm_hour:
        continue
    while datetime.datetime.now().minute != alarm_minute:
        continue
    bot.reply_to(message, f"ALARM! {event}")
    bot.send_sticker(message.chat.id, stickers_dict['STICKER_UNI_DONE'])

''' Not working T_T
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    delay_15 = types.KeyboardButton('15 minutes')
    delay_30 = types.KeyboardButton('30 minutes')
    keyboard.add(delay_15, delay_30)

    msg = bot.reply_to(message, 'Ok, I will remind you later', reply_markup=markup)
    bot.register_next_step_handler(msg, delay_handler)


def delay_handler(message):
    chat_id = message.chat.id
    if message.text == '15 minutes':
        print('call 15 min later')
        pass
    elif message.text == '30 minutes':
        print('call 30 min later')
        pass

    # keyboard.row('15 minutes', '30 minutes')
    #
    # minutes_15 = types.InlineKeyboardButton(text='15 minutes', callback_data='15');
    # minutes_30 = types.InlineKeyboardButton(text='30 minutes', callback_data='30');
    #
    # print(minutes_15, minutes_30)
    # alarm_minute += int(minutes_15)
'''

# USERS = set()


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