from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
from cogs import other
import requests
import sqlite3

OSU_ID = config.OSU_CLIENT_ID
OSU_SECRET = config.OSU_CLIENT_SECRET
X_API_VERSION = config.X_API_VERSION
OSU_USERS_DB = config.OSU_USERS_DB
TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

class Osu:
    def __init__(self, client_id, client_secret, x_api_version):
        url_token = 'https://osu.ppy.sh/oauth/token'
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials',
            'scope': 'public'
        }
        response = requests.post(url_token, data)
        self.__token = f'Bearer {response.json().get('access_token')}'
        self.base_url = 'https://osu.ppy.sh/api/v2'
        self.x_api_version = x_api_version
    def profile(self, user, mode='osu', params=None):
        user = f'@{user}'
        full_url = f'{self.base_url}/users/{user}/{mode}'
        __headers = {
            "Authorization": self.__token,
            "x-api-version": self.x_api_version,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        return requests.get(full_url, params, headers=__headers)


async def main(message):
    osu_api = Osu(OSU_ID, OSU_SECRET, X_API_VERSION)
    message_split = message.text.split(' ')
    message_split.pop(0)
    for i in range(3):
        message_split.append('$empty$')
    all_modes = ['std', 'osu', 'm', 'mania', 't', 'taiko', 'c', 'ctb', 'catch', 'fruits']
    flag = message_split[0]



    if flag is ('$empty$' or 'help'):
        text = """
*message format:* <prefix> <command> <option> <suffix>
*prefixes:* /osu, osu, o, su
*commands:* help, nick(set), profile(p), avatar

< > - required
( ) - optional

`su nick <username> (mode)` - set username
options: any username*(required)* and any mode

`su profile (username)` - check profile
options: you can write any other username
suffixes: osu(std), mania(m), taiko(t), fruits(c, ctb, catch)

`su avatar <username>` - returns avatar
options: any username*(required)*
        """
        await bot.reply_to(message, text, parse_mode='MARKDOWN')



    elif flag in ['p', 'profile']:
        if (message_split[1] not in all_modes) and (message_split[1] != '$empty$'):
            username = message_split[1]
        else:
            with sqlite3.connect(OSU_USERS_DB) as db:
                cursor = db.cursor()
                query = """ SELECT tg_id, osu_username FROM osu_users """
                cursor.execute(query)
                users = cursor.fetchall()
                for user in users:
                    if user[0] == message.from_user.id:
                        username = user[1]
                        pass
            try:
                username = username
            except:
                username = None


        mode = 'osu'
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = """ SELECT osu_username, osu_mode FROM osu_users """
            cursor.execute(query)
            mode_from_db = cursor.fetchall()
            for i in mode_from_db:
                if i[0] == username:
                    mode = i[1]
                    pass
        for i in all_modes:
            try:
                mode = message_split[message_split.index(i)]
            except:                                                                     #this block of code 
                pass                                                                    #define modes
        if mode == "std":
            mode = 'osu'
        elif mode == 'm':
            mode = 'mania'
        elif mode == 't':
            mode = 'taiko'
        elif mode is ('c' or 'ctb' or 'catch'):
            mode = 'fruits'


        if username != None:
            try:
                response = osu_api.profile(username,mode).json()
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton('profile url', f'https://osu.ppy.sh/users/{response['id']}')
                markup.add(button1)
                text = f'''
ID: {response['id']} 
Name: {response['username']} ({mode})
Global rank: #{response['statistics']['global_rank']}
Country rank: #{response['statistics']['rank']['country']}({response['country_code']})
PP: {response['statistics']['pp']}
Accuracy: {round(response['statistics']['hit_accuracy'], 2)}%
Play count: {response['statistics']['play_count']}
Play time: {response['statistics']['play_time']//86400}days {response['statistics']['play_time']//3600%24}hour {response['statistics']['play_time']//60%60}min ({response['statistics']['play_time'] // 60 // 60} hours)
Grades:
    SSH: {response['statistics']['grade_counts']['ssh']}
    SH: {response['statistics']['grade_counts']['sh']}
    SS: {response['statistics']['grade_counts']['ss']}
    S: {response['statistics']['grade_counts']['s']}
    A: {response['statistics']['grade_counts']['a']}
                '''
                await bot.send_photo(message.chat.id, response['cover']['url'],text , reply_to_message_id=message.id, reply_markup=markup)
            except:
                await bot.reply_to(message, "ERROR: username is not exists")
        else:
            await bot.reply_to(message, 'ERROR: write username OR set nick `su nick <username>`')



    elif flag in ['nick', 'set']:
        if message_split[1] != '$empty$':
            osu_username = message_split[1]
        else:
            await bot.reply_to(message, "ERROR: write username ```\nsu nick <your username>```", parse_mode='MARKDOWN')

        if message_split[2] != '$empty$':
            osu_mode = message_split[2]
        else:
            osu_mode = 'std'

        response = osu_api.profile(osu_username)
        try:
            with sqlite3.connect(OSU_USERS_DB) as db:
                cursor = db.cursor()
                osu_id = response.json()['id']
                tg_id = message.from_user.id
                tg_username = message.from_user.username
                query = """  CREATE TABLE IF NOT EXISTS osu_users(
                tg_id INTEGER UNIQUE,
                tg_username TEXT,
                osu_id INTEGER,
                osu_username TEXT,
                osu_mode TEXT
                )  """
                query1 = f""" REPLACE INTO osu_users (tg_id, tg_username, osu_id, osu_username, osu_mode) VALUES({tg_id}, '{tg_username}', {osu_id}, '{osu_username}', '{osu_mode}') """
                queries = [query, query1]
                for i in queries:
                    cursor.execute(i)
            await bot.reply_to(message, f'your username set, *{osu_username}*\nmode: *{osu_mode}*', parse_mode='MARKDOWN')
        except:
            await bot.reply_to(message, "ERROR: username is not exists")



    elif flag == 'avatar':
        user = message_split[1]
        if user != '$empty$':
            try:
                response = osu_api.profile(user)
                markup = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(f'{user} profile', f'https://osu.ppy.sh/users/{response.json()['id']}')
                button2 = types.InlineKeyboardButton(f'{user} avatar', response.json()['avatar_url'])
                button3 = types.InlineKeyboardButton(f'{user} cover', response.json()['cover_url'])
                markup.add(button1, row_width=1)
                markup.add(button2, button3, row_width=2)
                await bot.send_photo(message.chat.id, response.json()['avatar_url'], reply_to_message_id=message.id, reply_markup=markup)
            except:
                await bot.reply_to(message, 'ERROR: username is not exists')
        else:
            await bot.reply_to(message, 'ERROR: write username')



    elif flag == 'init':
        with sqlite3.connect(OSU_USERS_DB) as db:
            cursor = db.cursor()
            query = """  CREATE TABLE IF NOT EXISTS osu_users(
                tg_id INTEGER UNIQUE,
                tg_username TEXT,
                osu_id INTEGER,
                osu_username TEXT,
                osu_mode TEXT
                )  """
            cursor.execute(query)
        await bot.reply_to(message, 'initialization succesful')



    else:
        await bot.reply_to(message, "Incorrect command format")

print("Cogs | osu.py is ready")