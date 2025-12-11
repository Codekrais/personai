import asyncio
import time

import telebot.async_telebot as telebot
from deepseekcode1 import *
from allprompt import *
from dotenv import load_dotenv
import os
load_dotenv()

token = os.getenv("BOT_TOKEN")
admin_id = os.getenv("ADMIN_ID")
bot = telebot.AsyncTeleBot(token)

async def premes(message):
    sent_message = await bot.send_message(message.chat.id, '🕒Думаю над ответом...🕒')
    return sent_message.message_id


@bot.message_handler(commands=['log'])
async def ren(message):
    try:
        if message.from_user.id == admin_id:
            await bot.send_document(message.chat.id, open('datebase.json', 'rb'), caption=f'''Лог от [{current_time()}]:

Текущий api-ключ: {index_api_key}

База данных:''')
        else:
            await bot.send_message(message.chat.id, 'Вы не владеете правами администратора!')
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")


@bot.message_handler(commands=['ask'])
async def ren(message):
    try:
        nc = message.text.replace("/ask", "").strip().replace('', '').strip()

        if nc:
            # Отправляем сообщение о загрузке
            loading_msg_id = await premes(message)

            # Получаем ответ от нейросети
            res = await routerai(nc, get_prompt(message.chat.id))

            # Удаляем сообщение о загрузке и отправляем результат
            await bot.delete_message(message.chat.id, loading_msg_id)
            await bot.reply_to(message, res)
        else:
            await bot.reply_to(message, "Напишите сообщение после команды /ask")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(content_types=['photo'])
async def handle_photo(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{token}/{file_info.file_path}"
        loading_msg_id = await premes(message)
        res= await photoai(file_url, get_prompt(message.chat.id))
        await bot.delete_message(message.chat.id, loading_msg_id)
        await bot.reply_to(message, res)
    except Exception as e: await bot.reply_to(message, e)

@bot.message_handler(commands=['prompt'])
async def ren(message):
    try:

        nc = message.text.replace("/prompt", "").strip().replace('', '').strip()
        if nc:
            change_prompt(message.chat.id, nc)
            await bot.send_message(message.chat.id, "Промпт для вашего чата успешно изменён")
        else:
            await bot.send_message(message.chat.id, "Напишите промпт после команды /prompt")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['default'])
async def ren(message):
    try:
        reset_prompt(message.chat.id)
        await bot.send_message(message.chat.id, "Промпт для вашего чата успешно сброшен")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['check'])
async def ren(message):
    try:
        prompt = get_prompt_for_cmd(message.chat.id)
        if prompt:
            await bot.send_message(message.chat.id, f"{prompt}")
        elif not prompt:
            await bot.send_message(message.chat.id, f"У бота не установлена личность, чтобы получить список личностей пропишите\n/persons\n\n\
Чтобы задать личность введите\n/persona (личность)\n\n\
Если вы хотите установить кастомный промпт, то пропишите\n/prompt (сам промпт)")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['start'])
async def ren(message):
    try:
        await bot.send_message(message.chat.id, 'Я бот, который может менять личность.\
Вы можете использовать предустановленные личности /personа , или задать свою\n/prompt\n\
Задать вопрос ИИ /ask\n\n\
Разработчик текущей версии: <i>@endurra</i>\n\nПроцесс разработки и полезная информация: <i>@codebykrais</i>', parse_mode='HTML')
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['persona'])
async def ren(message):
    try:
        nc = message.text.replace("/persona", "").strip().replace('@personaiofficial_bot', '').strip()
        if nc:
            txt = change_person(message.chat.id, nc)
            await bot.send_message(message.chat.id, txt)
        else:
            await bot.send_message(message.chat.id, f"Напишите /persona (личность)\n\n\
Список личностей:\n\n{get_persons()}")
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['persons'])
async def ren(message):
    try:
        await bot.send_message(message.chat.id, f'Список личностей:\n\n{get_persons()}')
    except Exception as e:
        await bot.reply_to(message, f"Произошла ошибка: {str(e)}")

async def main():
    while True:
        try:
            print("Бот запущен в асинхронном режиме!")
            await bot.delete_webhook(drop_pending_updates=True)
            print("Вебхуки удалены")
            await bot.polling()
        except Exception as e:
            print(f'[{current_time()}] Ошибка: {e}')
            pass


if __name__ == "__main__":
    asyncio.run(main())