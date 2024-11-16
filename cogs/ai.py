from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
from cogs import other
import json
from llama_cpp import Llama


TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

ai_model = config.AI_MODEL              #
ai_maxtoken = config.AI_MAXTOKEN        #constants for this module
ai_const = config.AI_CONST              #
ai_threads = config.AI_THREADS          #
ai_b_threads = config.AI_B_THREADS      #
ai_context = config.AI_CONTEXT_TOKEN    #
ai_max_history = config.AI_MAX_HISTORY  #
llm = Llama(                        #parameters
    model_path = ai_model,          #ai gguf model
    chat_format="llama-3",          #idk
    verbose=False,                  #trash in command stroke
    n_threads=ai_threads,           #how much use cpu threads
    n_threads_batch=ai_b_threads,   #how much threads use for history
    n_ctx=ai_context
)

async def main(message):
    other.gtm(message)
    request = message.text.split(" ")  #
    request.pop(0)                     # prompt for ai
    request = " ".join(request)        #
    if len(request) > 1:                        #check prompt
        with open(config.AI_HISTORY, 'r') as file:          #get a history
            ai_history = json.load(file)                    #
            if str(message.chat.id) not in ai_history:                                                  #check chat id in history
                ai_history.setdefault(str(message.chat.id), [{"role": "system", "content": ai_const}])  #if no, it add id in dict
        ai_history_full = ai_history                            #converting history
        ai_history = ai_history[f'{message.chat.id}']           #
        ai_history.append({"role": "user", "content": request})                                 #add request to history
        if len(ai_history) > ai_max_history:                                   #
            for i in range(4):                                                 #delete a old history if it reach maximum
                ai_history.pop(1)                                              #
        await bot.send_chat_action(message.chat.id, "typing")                                   #change status to 'typing'
        output = llm.create_chat_completion(ai_history, max_tokens=ai_maxtoken)                 #ai response
        ai_history.append(output['choices'][0]['message'])                                      #add to history
        try:                                                                                                #trying to
            await bot.reply_to(message, output["choices"][0]["message"]["content"], parse_mode="MARKDOWN")  #send response
        except:                                                                                             #with parse
            await bot.reply_to(message, output["choices"][0]["message"]["content"])                         #markdown
        with open(config.AI_HISTORY,'w') as file:                   #
            ai_history_full[f'{message.chat.id}'] = ai_history      # return new history
            json.dump(ai_history_full, file)                        #
    else:                                                   #if no prompt
        await bot.reply_to(message, "ERROR: no prompt")     #

print("Cogs | ai.py is ready")