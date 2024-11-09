from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from cogs import other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN, "MARKDOWN")


async def main(message):
    other.gtm(message)
    await bot.send_message(message.chat.id, 
    """*Hello*
    My commands:
    /weather (city)(-a, -p)
    /game (-b, -d, -f, -bl, -s)""")

print("Cogs | start.py is ready")