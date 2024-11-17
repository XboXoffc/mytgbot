from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from cogs import other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)


async def main(message):
    other.gtm(message)
    text = """
*Hello*
My commands:
/about
/weather (city)(-a, -p)
/game (-b, -d, -f, -bl, -s)
/math (num)(-sqrt, -sqr, -sin, -cos, -tg)
/ai_assist (prompt)
Check my github for docs in /about
"""
    try:
        await bot.send_message(message.chat.id, text, "MARKDOWN")
    except:
        await bot.send_message(message.chat.id, text)
print("Cogs | start.py is ready")