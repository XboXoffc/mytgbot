from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
from cogs import other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    other.gtm(message)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("DonationAlerts", "https://www.donationalerts.com/r/xbox202")
    markup.add(button1)
    text = """
You can help me financially(with donate) or message me(@xbox202) any your idea
"""
    await bot.send_message(message.chat.id, text, reply_markup=markup)


print("Cogs | support.py is ready")