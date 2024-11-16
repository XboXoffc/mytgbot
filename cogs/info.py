from telebot.async_telebot import AsyncTeleBot
import asyncio
import config
from cogs import other
from telebot import types

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

async def main(message):
    other.gtm(message)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("About bot", callback_data="about_bot")
    button2 = types.InlineKeyboardButton("Contacts", callback_data="contacts")
    markup.add(button1, button2)
    text = """
Choose any you need
"""
    await bot.reply_to(message, text, reply_markup=markup)

async def callback(call):
    if call.data == "about_bot":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Bot code(github)", "https://github.com/XboXoffc/mytgbot")
        markup.add(button1)
        text = """
Just pet project
There you can check weather and etc
"""
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
    if call.data == "contacts":
        text = """
dev: @xbox202
Write me if bot don't work correctly        
"""
        await bot.send_message(call.message.chat.id, text)

print("Cogs | info.py is ready")