from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from cogs import other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    other.gtm(message)
    if "-basket" in message.text or "-b" in message.text:
        await bot.send_dice(message.chat.id, "🏀")
    elif "-darts" in message.text or "-d" in message.text:
        await bot.send_dice(message.chat.id, "🎯")
    elif "-football" in message.text or "-f" in message.text:
        await bot.send_dice(message.chat.id, "⚽")
    elif "-bowling" in message.text or "-bl" in message.text:
        await bot.send_dice(message.chat.id, "🎳")
    elif "-slots" in message.text or "-s" in message.text:
        await bot.send_dice(message.chat.id, "🎰")
    else:
        await bot.send_dice(message.chat.id)

print("Cogs | dice.py is ready")