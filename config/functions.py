from telegram import (
    Update,
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    KeyboardButton, 
    ReplyKeyboardMarkup
)
from telegram.ext import (
    CallbackContext
)

from .list import filters_list
from .db import db

async def make_buttons(buttons_list):
    keyboard = []
    keyboard_second = []

    for button_text, callback_data in buttons_list:
        if 'http' in callback_data:
            button = InlineKeyboardButton(text=button_text, url=callback_data)
        elif 'Порекомендовать бот' in button_text:
            button = InlineKeyboardButton(text=button_text, switch_inline_query=callback_data)
        else:
            button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
        keyboard_second.append(button)
        if callback_data == '#':
            keyboard.append(keyboard_second)
            keyboard_second = []
    keyboard.append(keyboard_second)
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def keyboard(button_text):
    keyboard = []
    row = []
    for button in button_text:
        if button == '#':
            if row:
                keyboard.append(row)
                row = []
        else:
            row.append(KeyboardButton(button))
    if row:
        keyboard.append(row)
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


async def get_data(update: Update, context: CallbackContext):
    
    result_list = {}

    text_list = update.message.text.split('\n')

    result_list['group_id'] = update.effective_chat.id
    result_list['date'] = text_list[0]
    result_list['fio'] = text_list[1]

    text_list = update.message.text.replace(" ", "").split('\n')

    coun = 0
    for i in text_list[2:]:
        try:
            result_list[f'spare{coun+1}'] = i.split(filters_list[coun])[1].replace("-", "")
            coun += 1
        except IndexError:
            break
        except Exception as e:
            print(f'Error: {e=}')

    db.add_data(result_list)
    print(f'{result_list=}')



