from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
from cogs import other
from llama_cpp import Llama

TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN, "MARKDOWN")

ai_model = config.AI_MODEL
ai_maxtoken = config.AI_MAXTOKEN
llm = Llama(
    model_path = ai_model,
    chat_format="llama-3"
)
ai_const = config.AI_CONST
ai_history = [{"role": "system", "content": ai_const}]

async def main(message):
    other.gtm(message)
    work = True
    request = message.text.split(" ")
    request.pop(0)
    request = " ".join(request)
    if len(request) > 1:
        ai_history.append({"role": "user", "content": request})
        await bot.send_chat_action(message.chat.id, "typing")
        output = llm.create_chat_completion(ai_history, max_tokens=ai_maxtoken)
        ai_history.append(output["choices"][0]["message"])
        await bot.reply_to(message, output["choices"][0]["message"]["content"] )
        for i in range(1,3): ai_history.pop(1)
    else:
        await bot.reply_to(message, "ERROR: no prompt")

print("Cogs | ai.py is ready")