from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests
import config
from cogs import start, info, game, weather, math, ai, other

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
async def Start(message):
    await start.main(message)

@bot.message_handler(commands=["info", "about"])
async def Info(message):
    await info.main(message)

@bot.message_handler(commands=["game"])
async def Game(message):
    await game.main(message)

@bot.message_handler(commands=["weather"])
async def Weather(message):
    await weather.main(message)

@bot.message_handler(commands=["math"])
async def Math(message):
    await math.main(message)

@bot.message_handler(commands=["ai_assist"])
async def Ai(message):
    await ai.main(message)

@bot.callback_query_handler(func=lambda call:True)
async def Callback(call):
    await info.callback(call)

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'sticker', 'location'])
async def echo_message(message):
    other.gtm(message)

print("Bot | already started\n\n")
asyncio.run(bot.polling(non_stop=True))
