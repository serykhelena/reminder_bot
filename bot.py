import telebot
from telebot.types import Message
import random
# import requests

with open('bot_token.txt', 'r') as vip_file:
    TOKEN = vip_file.read()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def echo_digits(message: Message):
    bot.reply_to(message, str(random.random( )))


bot.polling(timeout=60)


'''
# MAIN_URL = f'https://api.telegram.org/bot{TOKEN}'

payload = {
    'chat_id': 133919098,
    'text': ' Hi, Lena!',
    'reply_to_message_id': 3
}

r = requests.post(f'{MAIN_URL}/sendMessage', data=payload)

# r = requests.get(f'{MAIN_URL}/getUpdates')

print(r.json())
'''