from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests

TOKEN = "YOUR TOKEN"
API_KEY = "YOUR TOKEN" #IN https://www.weatherapi.com/
bot = AsyncTeleBot(TOKEN, "MARKDOWN")

@bot.message_handler(commands=["start"], chat_types="private")
async def start(message):
    await bot.send_message(message.chat.id, 
    """*Hello*
    My commands:
    /weather (city)
    /dice""")

@bot.message_handler(commands=["dice"], chat_types="private")
async def dice(message):
    await bot.send_dice(message.chat.id)

@bot.message_handler(commands=["weather"])
async def weather(message):
    message_split = message.text.split(" ")
    city = message_split[1]
    days = 2
    api_key=API_KEY
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": city,
        "days": days
    }
    response = requests.get(base_url, params)
    if response.status_code == 200:
        data = response.json()
        location = data["location"]
        current = data["current"]
        forecast = data["forecast"]["forecastday"]
        text = f"""*{location["localtime"]}*
*{location["country"]}, {location["region"]}, {location["name"]}*
*Current:*
    {current["condition"]["text"]}
    temp: {current["temp_c"]}°C
    rain chance: {forecast[0]["day"]["daily_chance_of_rain"]}%

*Tomorrow({forecast[1]["date"]}):*
    {forecast[1]["day"]["condition"]["text"]}
    max temp: {forecast[1]["day"]["maxtemp_c"]}°C
    min temp: {forecast[1]["day"]["mintemp_c"]}°C
    avg temp: {forecast[1]["day"]["avgtemp_c"]}°C
    rain chance: {forecast[1]["day"]["daily_chance_of_rain"]}%"""
        await bot.send_message(message.chat.id, text)
    else:
        await bot.send_message(message.chat.id, f"api is not work {response}")

asyncio.run(bot.polling(non_stop=True))
