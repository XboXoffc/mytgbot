from telebot.async_telebot import AsyncTeleBot
from telebot import types
import asyncio
import config
from cogs import other
import json
from llama_cpp import Llama


TOKEN = config.TG_TOKEN
bot = AsyncTeleBot(TOKEN)

ai_model = config.AI_MODEL                  #
ai_maxtoken = config.AI_MAXTOKEN            #constants for this module
ai_const = config.AI_CONST                  #
ai_threads = config.AI_THREADS              #
ai_b_threads = config.AI_B_THREADS          #
ai_context = config.AI_CONTEXT_TOKEN        #
ai_max_history = config.AI_MAX_HISTORY      #
ai_logs = config.AI_LOGS                    #
ai_user_maxtoken = config.AI_USER_MAXTOKEN  #
llm = Llama(                        #parameters
    model_path = ai_model,          #ai gguf model
    chat_format="llama-3",          #idk
    verbose=ai_logs,                #trash in command stroke
    n_threads=ai_threads,           #how much use cpu threads
    n_threads_batch=ai_b_threads,   #how much threads use for history
    n_batch=ai_user_maxtoken,
    n_ctx=ai_context
)

async def main(message):
    other.gtm(message)

    request = message.text.split(" ")  #
    request.pop(0)                     # prompt for ai
    request = " ".join(request)        #

    delete_history = False
    if "-del" in request:
        delete_history = True
        request = request.split(" ")
        request.pop(request.index('-del'))
        request = " ".join(request)

    anonimous_mode = False
    if '-anon' in request:
        anonimous_mode = True
        request = request.split(' ')
        request.pop(request.index('-anon'))
        request = " ".join(request)

    history_enable = True       #
    if ai_max_history <= 0:     #check history disable
        history_enable = False  #

    if len(request) > 1:             #check prompt
        if history_enable and not anonimous_mode:
            try:
                with open(config.AI_HISTORY, 'r') as file:                                                      #get a history
                    ai_history = json.load(file)                                                                #
                    if str(message.chat.id) not in ai_history:                                                  #check chat id in history
                        ai_history.setdefault(str(message.chat.id), [{"role": "system", "content": ai_const}])  #if no, it add id in dict
            except:
                with open(config.AI_HISTORY, 'x') as file:                                                      #create ai history file
                    file.write('{}')                                                                            #for json
                with open(config.AI_HISTORY, 'r') as file:                                                      #
                    ai_history = json.load(file)                                                                #
                    ai_history.setdefault(str(message.chat.id), [{"role": "system", "content": ai_const}])      #add new history for chat id

            ai_history_full = ai_history                                    #converting history
            ai_history = ai_history[f'{message.chat.id}']                   #
            if delete_history:                                              #if there is -del
                ai_history = [{"role": "system", "content": ai_const}]      #delete history
                ai_history.append({"role": "user", "content": request})     #add temp history (because history will not save)
            else:                                                           #else
                ai_history.append({"role": "user", "content": request})     #add request to history

            if len(ai_history) > ai_max_history:                     #
                for i in range(4):                                   #delete a old history if it reach maximum
                    ai_history.pop(1)                                #
        else:                                                           #if history disabled or request anonymous
            ai_history = [{"role": "system", "content": ai_const}]      #add temp history list
            ai_history.append({"role": "user", "content": request})     #add request to history

        try:
            await bot.send_chat_action(message.chat.id, "typing")                                     #change status to 'typing'
            output = llm.create_chat_completion(ai_history, max_tokens=ai_maxtoken)                   #ai response
            try:                                                                                                #trying to
                await bot.reply_to(message, output["choices"][0]["message"]["content"], parse_mode="MARKDOWN")  #send response
            except:                                                                                             #with parse
                await bot.reply_to(message, output["choices"][0]["message"]["content"])                         #markdown

            if history_enable and not anonimous_mode:                                         
                ai_history.append(output['choices'][0]['message'])          # add to history
                with open(config.AI_HISTORY,'w') as file:                   #
                    ai_history_full[f'{message.chat.id}'] = ai_history      # return new history
                    json.dump(ai_history_full, file)                        #
        except Exception as error:
            bot.reply_to(message, f"ServerError:\n{error}")
    else:                                                   #if no prompt
        await bot.reply_to(message, "ERROR: no prompt")     #

print("Cogs | ai.py is ready")