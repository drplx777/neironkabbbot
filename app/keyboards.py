from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Чат')],
                                     [KeyboardButton(text='Генерация картинок')],
                                     [KeyboardButton(text='Пополнить баланс')]],
                           resize_keyboard=True, 
                           input_field_placeholder='Выберите пункт меню')



cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]], resize_keyboard=True)

credits = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Telegram', url='https://t.me/drplx')], [InlineKeyboardButton(text='Vk', url='https://vk.com/driplexxx')]])