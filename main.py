from telebot.async_telebot import AsyncTeleBot
import asyncio
import requests

TOKEN = "YOUR TOKEN"
API_KEY = "YOUR TOKEN" #https://www.weatherapi.com/
bot = AsyncTeleBot(TOKEN, "MARKDOWN")



@bot.message_handler(commands=["start", "help"], chat_types="private")
async def start(message):
    gtm(message)
    await bot.send_message(message.chat.id, 
    """*Hello*
    My commands:
    /weather (city)
    /dice""")

@bot.message_handler(commands=["dice"], chat_types="private")
async def dice(message):
    gtm(message)
    await bot.send_dice(message.chat.id)

@bot.message_handler(commands=["weather"])
async def weather(message):
    gtm(message)
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
    snow chance: {forecast[0]["day"]["daily_chance_of_snow"]}%
*Tomorrow({forecast[1]["date"]}):*
    {forecast[1]["day"]["condition"]["text"]}
    max temp: {forecast[1]["day"]["maxtemp_c"]}°C
    min temp: {forecast[1]["day"]["mintemp_c"]}°C
    avg temp: {forecast[1]["day"]["avgtemp_c"]}°C
    rain chance: {forecast[1]["day"]["daily_chance_of_rain"]}%
    snow chance: {forecast[1]["day"]["daily_chance_of_snow"]}%"""
        await bot.send_message(message.chat.id, text)
    else:
        await bot.send_message(message.chat.id, f"api is not work {response}")

#Подслушка
def gtm(message):
    if message.text:
        print('Пользователь {}, {} написал: {}'.format(message.from_user.id, message.from_user.first_name, message.text))
    elif message.photo:
        print('Пользователь {}, {} отправил фото: {}'.format(message.from_user.id, message.from_user.first_name, message.photo[0].file_id))
    elif message.sticker:
        print('Пользователь {}, {} отправил стикер: {}'.format(message.from_user.id, message.from_user.first_name, message.sticker.emoji))
    elif message.location:
        print('Пользователь {}, {} отправил локацию'.format(message.from_user.id, message.from_user.first_name))
        
@bot.message_handler(content_types=['text', 'photo', 'document', 'audio', 'video', 'sticker',
                    'location', 'contact', 'voice', 'poll', 'poll_answer', 'dice', 'game'],
                    chat_types=['private'])
async def echo_message(message):
    gtm(message)

@bot.message_handler(func=lambda message: True, content_types=['text', 'location'])
async def echo_message2(message):
    gtm(message)



print("Бот запущен")
asyncio.run(bot.polling(non_stop=True))
