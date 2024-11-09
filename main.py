from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests
import config
from cogs import start, game, weather, other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN, "MARKDOWN")


@bot.message_handler(commands=["start", "help"])
async def Start(message):
    await start.main(message)

@bot.message_handler(commands=["game"])
async def Game(message):
    await game.main(message)

@bot.message_handler(commands=["weather"])
async def Weather(message):
    await weather.main(message)
        
@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'location'])
async def echo_message(message):
    other.gtm(message)

print("Bot | already started")
asyncio.run(bot.polling(non_stop=True))
