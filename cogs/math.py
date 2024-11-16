from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from cogs import other
from telebot import types
import math

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    other.gtm(message)
    if message.text.split(" ")[1] != str:
        try:
            question = int(message.text.split(" ")[1])
        except:
            question = float(message.text.split(" ")[1])
        flags = message.text.split(" ")
        if "-sqrt" in flags or "-root" in flags:
            text = f"Result: {math.sqrt(question)}"
            print(text)
            await bot.reply_to(message, text)
        elif "-sqr" in flags or "-square" in flags:
            text = f"Result: {question ** 2}"
            print(text)
            await bot.reply_to(message, text)
        elif "-sin" in flags:
            text = f"Result: {math.sin(math.radians(question))}"
            print(text)
            await bot.reply_to(message, text)
        elif "-cos" in flags or "-cosine" in flags:
            text = f"Result: {math.cos(math.radians(question))}"
            print(text)
            await bot.reply_to(message, text)
        elif "-tan" in flags or "-tg" in flags or "-tangent" in flags:
            text = f"Result: {math.tan(math.radians(question))}"
            print(text)
            await bot.reply_to(message, text)
        else:
            text = f"ERROR: Write flag"
            await bot.reply_to(message, text)
    else:
        bot.reply_to(message, "ERROR: incorrect syntax")


print("Cogs | math.py is ready")