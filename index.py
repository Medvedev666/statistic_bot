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
    get_data, error_data
)
from config.list import filters_list, months_dict, spare_columns, help_str, commands
from config.db import db

import os
import re
from datetime import datetime



application = ApplicationBuilder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat.type == 'private':
        db.add_user(update.message.from_user.id, update.message.from_user.username)


    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                            text=f'Приветствую <b>{update.message.from_user.first_name}</b> 🤝'
                            '\nКоманды для взаимодействия:\n\n'
                            f'{help_str}', parse_mode=ParseMode.HTML)


async def commands_func(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    for c in commands:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'{c}', parse_mode=ParseMode.HTML)


async def show_all(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_all {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_all вышли')
        return

    result = db.get_spars(data=None, index=None, fio=None)
    logger.info(f'{result=}')

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Таблица пуста')
    
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
                                text=f'<b>/show_day дд.мм.гггг</b>',
                                parse_mode=ParseMode.HTML)
    logger.info(f'{day=}')

    result = db.get_spars(data=day, index="day", fio=None)
    logger.info(f'{result=}')

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {day}\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{day[-4:]}')



async def show_week(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_week {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_week вышли')
        return

    result = db.get_spars(data=None, index="week", fio=None)
    logger.info(f'{result=}')

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за последние 7 дней\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f"#{datetime.now().strftime('%Y')}г")



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
                                text=f'<b>/show_mes мм.гггг</b>',
                                parse_mode=ParseMode.HTML)

    result = db.get_spars(data=mes, index="mes", fio=None)
    logger.info(f'{result=}')

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {months_dict[mes[:2]]}\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{mes[-4:]}г')
    


async def show_year(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_year {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_year вышли')
        return

    year = update.message.text.replace('/show_year', '').replace(' ', '')
    date_pattern = r"^\d{4}$"

    if year == '' or not re.match(date_pattern, year):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Введите команду в формате:',
                                parse_mode=ParseMode.HTML)
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'<b>/show_year гггг</b>',
                                parse_mode=ParseMode.HTML)

    result = db.get_spars(data=year, index="year", fio=None)
    logger.info(f'{result=}')

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')

    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {year}г\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{year}г')    



async def show_day_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_day_users {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_day_users вышли')
        return

    day_and_list = update.message.text.replace('/show_day_users', '').strip() # /show_day_users 15.07.2024 Галя Иванова, Никита
    day = day_and_list[:10]
    date_pattern = r"^\d{2}\.\d{2}\.\d{4}$"

    if day == '' or not re.match(date_pattern, day):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Введите команду в формате:',
                                parse_mode=ParseMode.HTML)
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'<b>/show_day_users дд.мм.гггг Фамилия Имя, Фамилия Имя ...</b>',
                                parse_mode=ParseMode.HTML)
    logger.info(f'{day=}')

    fio_list = [item.strip() for item in day_and_list.replace(day, '').split(',')]
    
    result = db.get_spars(data=day, index="usersday", fio=fio_list) 
    logger.info(f'{result=}')

    fio_string = ', '.join(fio_list)

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')

    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {day} для {fio_string}\n\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{day[-4:]}')



async def show_week_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_week_users {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_week_users вышли')
        return

    fio_list = update.message.text.replace('/show_week_users', '').strip()
    fio_list = [item.strip() for item in fio_list.split(',')]

    result = db.get_spars(data=None, index="usersweek", fio=fio_list)
    logger.info(f'{result=}')

    fio_string = ', '.join(fio_list)

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за последние 7 дней для {fio_string}\n\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f"#{datetime.now().strftime('%Y')}г")



async def show_mes_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_mes_users {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_mes_users вышли')
        return

    mes_and_list = update.message.text.replace('/show_mes_users', '').strip() # /show_mes_users 07.2024 Галя Иванова, Никита
    mes = mes_and_list[:7]
    date_pattern = r"^\d{2}\.\d{4}$"

    if mes == '' or not re.match(date_pattern, mes):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Введите команду в формате:',
                                parse_mode=ParseMode.HTML)
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'<b>/show_mes_users мм.гггг Фамилия Имя, Фамилия Имя ...</b>',
                                parse_mode=ParseMode.HTML)
    
    fio_list = [item.strip() for item in mes_and_list.replace(mes, '').split(',')]

    result = db.get_spars(data=mes, index="usersmes", fio=fio_list)
    logger.info(f'{result=}')

    fio_string = ', '.join(fio_list)

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {months_dict[mes[:2]]} для {fio_string}\n\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{mes[-4:]}г')
    


async def show_year_users(update: Update, context: ContextTypes.DEFAULT_TYPE):

    logger.info(f'show_year_users {update.effective_chat.id=}')
    if update.effective_chat.id not in GROUPS_ID:
        logger.info(f'show_year_users вышли')
        return

    year_and_list = update.message.text.replace('/show_year_users', '').strip() # /show_year_users 2024 Галя Иванова, Никита
    year = year_and_list[:4]
    date_pattern = r"^\d{4}$"

    if year == '' or not re.match(date_pattern, year):
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Введите команду в формате:',
                                parse_mode=ParseMode.HTML)
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'<b>/show_year_users гггг Фамилия Имя, Фамилия Имя ...</b>',
                                parse_mode=ParseMode.HTML)

    fio_list = [item.strip() for item in year_and_list.replace(year, '').split(',')]

    result = db.get_spars(data=year, index="usersyear", fio=fio_list)
    logger.info(f'{result=}')

    if all(result[column] == '' for column in spare_columns):
        return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'По данным параметрам ничего не найдено')
    
    fio_string = ', '.join(fio_list)
    
    return await context.bot.send_message(chat_id=update.effective_chat.id, 
                                text=f'Статистика за {year}г для {fio_string}\n\n'
                                f"1. Количество звонков - {result['spare1']}\n"
                                f"2. Да на 1 - ю встречу - {result['spare2']}\n"
                                f"3. Количество 1 встреч - {result['spare3']}\n"
                                f"4. Количество на вторую встречу - {result['spare4']}\n"
                                f"5. Количество 2х встреч - {result['spare5']}\n"
                                f"6. Товарооборот - {result['spare6']}\n"
                                f'#{year}г')    



async def idnw_message(update: Update, context: CallbackContext): 

    if update.effective_chat.id in GROUPS_ID:
        logger.info('idnw_message вышли')
        return

    cleaned_mes = update.message.text.replace(" ", "")
    match all(val in cleaned_mes for val in filters_list):
        case True:
            await get_data(update, context)
        case _:
            await error_data(update, context)
    


def main():
    start_handler = CommandHandler('start', start)
    commands_handler = CommandHandler('commands', commands_func)

    show_all_handler = CommandHandler('show_all', show_all)
    show_day_handler = CommandHandler('show_day', show_day)
    show_week_handler = CommandHandler('show_week', show_week)
    show_mes_handler = CommandHandler('show_mes', show_mes)
    show_year_handler = CommandHandler('show_year', show_year)
    

    show_day__users_handler = CommandHandler('show_day_users', show_day_users)
    show_week_users_handler = CommandHandler('show_week_users', show_week_users)
    show_mes_users_handler = CommandHandler('show_mes_users', show_mes_users)
    show_year_users_handler = CommandHandler('show_year_users', show_year_users)

    idnw_henler = MessageHandler(filters.ALL, idnw_message)

    
    application.add_handler(start_handler)
    application.add_handler(commands_handler)

    application.add_handler(show_all_handler)
    application.add_handler(show_day_handler)
    application.add_handler(show_week_handler)
    application.add_handler(show_mes_handler)
    application.add_handler(show_year_handler)

    application.add_handler(show_day__users_handler)
    application.add_handler(show_week_users_handler)
    application.add_handler(show_mes_users_handler)
    application.add_handler(show_year_users_handler)

    application.add_handler(idnw_henler)

    application.run_polling()

if __name__ == '__main__':
    main()