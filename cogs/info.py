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
    button3 = types.InlineKeyboardButton("Support", callback_data="support")
    button4 = types.InlineKeyboardButton("Credits", callback_data="credits")
    markup.add(button1, button2, button3, button4, row_width=2)
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
    if call.data == 'support':
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("DonationAlerts", "https://www.donationalerts.com/r/xbox202")
        markup.add(button1)
        text = """
You can help me financially(with donate) or message me(@xbox202) any your idea
"""
        await bot.send_message(call.message.chat.id, text, reply_markup=markup)
    if call.data == 'credits':
        text ="""
Thanks for imexoQQ(ilmir) for host my bot
"""
        await bot.send_message(call.message.chat.id, text)

print("Cogs | info.py is ready")