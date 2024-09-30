import os
import telebot
import requests
import json
import urllib.parse
import asyncio
from dotenv import load_dotenv
load_dotenv()

bot = telebot.TeleBot(os.getenv("Telegram_API_KEY"))

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    aisay = requests.post('http://localhost:8000/chat?query=你好陈师傅!')
    aisay = json.loads(aisay.text)
    print(aisay)
    text_without_quotes = aisay["msg"]["output"].strip('"')
    bot.reply_to(message, text_without_quotes.encode('utf-8'))

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        encoded_text = urllib.parse.quote(message.text)
        aisay_response = requests.post('http://localhost:8000/chat?query=' + encoded_text, timeout=100)  # 设置超时
        if aisay_response.status_code == 200:
            aisay = json.loads(aisay_response.text)
            if "msg" in aisay:
                bot.reply_to(message, aisay["msg"]["output"].encode('utf-8'))
                audio_path = f"/audio/{aisay['id']}.mp3"
                print(audio_path)
                asyncio.run(check_audio(message, audio_path))
                
            else:
                bot.reply_to(message, "server error!")
        else:
            bot.reply_to(message, "server error!")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        bot.reply_to(message, "对不起本大师似乎想休息一下!")

async def check_audio(message, audio_file):
    while True:
        if os.path.exists(audio_file):
            with open(audio_file, 'rb') as audio:
                bot.send_audio(message.chat.id, audio)
            os.remove(audio_file)
            break
        else:
            print("waiting for audio file...")
            await asyncio.sleep(1)  # 使用 asyncio.sleep 而不是 time.sleep


bot.infinity_polling()