#!/usr/bin/python

import telebot
import datetime
from datetime import date

with open('bot_token.txt', 'r') as vip_file:
    TOKEN = vip_file.read()

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



#
# @bot.message_handler(content_types=['text'])
# @bot.edited_message_handler(content_types=['text'])
# def bot_welcome(message: Message):
#     if 'Bot' in message.text:
#         bot.reply_to(message, "I'm ready, my dear")
#         bot.send_sticker(message.chat.id, stickers_dict['STICKER_KAPI_HI'])


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
                 f'You can set time and event only for today {date_now}\n'
                 'Now give me time and name of event that you want I remind you'
                 )


@bot.message_handler(content_types=['text'])
@bot.edited_message_handler(content_types=['text'])
def event_handler(message):
    if 'Hi' in message.text:
        bot.reply_to(message, "Hello ^_____^")
        bot.send_sticker(message.chat.id, stickers_dict['STICKER_KAPI_HI'])
    elif 'set' in message.text:
        radz_indx = message.text.find(':')
        alarm_hour = int(''.join(c for c in message.text[:radz_indx] if c.isdigit()))
        alarm_minute = int(''.join(c for c in message.text[radz_indx:] if c.isdigit()))

        remind_msg = message.text[radz_indx+4:]

        while datetime.datetime.now().hour != alarm_hour:
            continue
        while datetime.datetime.now().minute != alarm_minute:
            continue
        bot.reply_to(message, remind_msg)
        bot.send_sticker(message.chat.id, stickers_dict['STICKER_UNI_DONE'])


bot.polling(timeout=60)

