from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, 
    ContextTypes, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackContext, 
)
from telegram.constants import ParseMode

from config.config import TOKEN, logger, GROUPS_ID
from config.functions import (
    make_buttons, keyboard,
    get_data
)
from config.list import filters_list, months_dict
from config.db import db

import os
import re



application = ApplicationBuilder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_chat.id not in GROUPS_ID:
        return

    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Приветствую\nКоманды для взаимодействия:\n'
                                '')

async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_all {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_all вышли')
        return

    result = db.get_spars(data=None, index=None)
    logger.info(f'{result=}')
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за все время\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}")

async def show_day(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_day {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_day вышли')
        return

    day = update.message.text.replace('/show_day', '').replace(' ', '')
    date_pattern = r"^\d{2}\.\d{2}\.\d{4}$"

    if day == '' or not re.match(date_pattern, day):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Введите команду в формате:',
                                parse_mode=ParseMode.HTML)
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'<b>/show_day дд.мм.гг</b>',
                                parse_mode=ParseMode.HTML)
    logger.info(f'{day=}')

    result = db.get_spars(data=day, index="day")
    logger.info(f'{result=}')
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {day}\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{day[-4:]}')
                                

async def show_mes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_mes {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_mes вышли')
        return

    mes = update.message.text.replace('/show_mes', '').replace(' ', '')
    date_pattern = r"^\d{2}\.\d{4}$"

    if mes == '' or not re.match(date_pattern, mes):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Введите команду в формате:',
                                parse_mode=ParseMode.HTML)
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'<b>/show_mes мм.гг</b>',
                                parse_mode=ParseMode.HTML)

    result = db.get_spars(data=mes, index="mes")
    logger.info(f'{result=}')
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {months_dict[mes[:2]]}\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{mes[-4:]}г')
    

async def idnw_message(update: Update, context: CallbackContext): 

    if update.effective_chat.id in GROUPS_ID:
        logger.info('idnw_message вышли')
        return

    cleaned_mes = update.message.text.replace(" ", "")
    match all(val in cleaned_mes for val in filters_list):
        case True:
            await get_data(update, context)
        case _:
            logger.info(f'{cleaned_mes=}')
            
            return await context.bot.send_message(chat_id='-1002247298434', 
                                text=f'Ответ не по шаблону, запись не сделана, группа: {update.effective_chat.id}')
    


def main():
    start_handler = CommandHandler('start', start)
    show_all_handler = CommandHandler('show_all', show_all)
    show_day_handler = CommandHandler('show_day', show_day)
    show_mes_handler = CommandHandler('show_mes', show_mes)
    idnw_henler = MessageHandler(filters.ALL, idnw_message)

    
    application.add_handler(start_handler)
    application.add_handler(show_all_handler)
    application.add_handler(show_day_handler)
    application.add_handler(show_mes_handler)
    application.add_handler(idnw_henler)

    application.run_polling()

if __name__ == '__main__':
    main()