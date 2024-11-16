from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests
import config
from cogs import other

TOKEN = config.TG_TOKEN
API_KEY = config.WHEATHER_API
bot = AsyncTeleBot(TOKEN)

async def main(message):
    other.gtm(message)
    message_split = message.text.split(" ")
    try:
        city = message_split[1]
        flags = message_split
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
        #flags for weather
            if "-add" in flags or "-a" in flags:
                text = f"""*{location["localtime"]}*
*{location["country"]}, {location["region"]}, {location["name"]}*
*Current:*
    {current["condition"]["text"]}
    temp: {current["temp_c"]}°C
    rain chance: {forecast[0]["day"]["daily_chance_of_rain"]}%
    snow chance: {forecast[0]["day"]["daily_chance_of_snow"]}%
*Tomorrow({forecast[1]["date"]}):*
    {forecast[1]["day"]["condition"]["text"]}
    max temp: {forecast[1]["day"]["maxtemp_c"]}°C
    min temp: {forecast[1]["day"]["mintemp_c"]}°C
    avg temp: {forecast[1]["day"]["avgtemp_c"]}°C
    rain chance: {forecast[1]["day"]["daily_chance_of_rain"]}%
    snow chance: {forecast[1]["day"]["daily_chance_of_snow"]}%"""
                await bot.send_message(message.chat.id, text, "MARKDOWN")

            else:
                text = f"""*{location["localtime"]}*
*{location["country"]}, {location["region"]}, {location["name"]}*
    {current["condition"]["text"]}
    temp: {current["temp_c"]}°C
    rain chance: {forecast[0]["day"]["daily_chance_of_rain"]}%
    snow chance: {forecast[0]["day"]["daily_chance_of_snow"]}%"""
                await bot.send_message(message.chat.id, text, "MARKDOWN")
                
            if "-p" in flags:
                text = "it is easter egg -- pashalko"
                await bot.send_message(message.chat.id, text, "MARKDOWN")
        else:
            response = response.json()
            await bot.send_message(message.chat.id, f"api is not work\n{response}", timeout=20)
    except:
        await bot.send_message(message.chat.id, "Вы не указали город", timeout=5)


print("Cogs | weather.py is ready")